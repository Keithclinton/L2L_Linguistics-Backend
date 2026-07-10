from django.utils import timezone
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from courses.models import Course, Enrollment
from courses.access import has_course_access
from .models import Payment, Subscription
from . import mpesa
from .serializers import PaymentInitiateSerializer, PaymentSerializer


class InitiatePaymentView(APIView):
    """Starts an M-Pesa Daraja STK Push for either a one-off course payment
    (course_id) or an all-access subscription (plan)."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PaymentInitiateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number', '')
        plan = serializer.validated_data.get('plan')

        if plan:
            payment = Payment.objects.create(
                learner=request.user,
                course=None,
                amount=Subscription.PLAN_PRICES[plan],
                currency='KES',
                provider='mpesa',
                status='pending',
                phone_number=phone_number,
            )
            subscription = Subscription.objects.create(
                learner=request.user, plan=plan, payment=payment,
            )
            amount = payment.amount
            reference = f'SUB-{subscription.id}'
            description = f'Ufasaha Wa Lugha {subscription.get_plan_display()} subscription'
        else:
            course_id = serializer.validated_data['course_id']
            try:
                course = Course.objects.get(pk=course_id, is_published=True)
            except Course.DoesNotExist:
                return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

            if course.is_free:
                return Response({'detail': 'This course is free. Use the enroll endpoint.'}, status=status.HTTP_400_BAD_REQUEST)

            if has_course_access(request.user, course):
                return Response({'detail': 'You already have access to this course.'}, status=status.HTTP_400_BAD_REQUEST)

            payment = Payment.objects.create(
                learner=request.user,
                course=course,
                amount=course.price,
                currency='KES',
                provider='mpesa',
                status='pending',
                phone_number=phone_number,
            )
            amount = payment.amount
            reference = f'COURSE-{course.id}'
            description = f'Ufasaha Wa Lugha — {course.title}'

        try:
            result = mpesa.stk_push(
                phone_number=phone_number, amount=amount,
                account_reference=reference, description=description,
            )
        except Exception:
            payment.status = 'failed'
            payment.save(update_fields=['status'])
            return Response({'detail': 'Could not reach M-Pesa. Please try again.'}, status=status.HTTP_502_BAD_GATEWAY)

        payment.provider_reference = result.get('CheckoutRequestID', '')
        payment.save(update_fields=['provider_reference'])

        return Response({
            'payment_id': payment.id,
            'checkout_request_id': result.get('CheckoutRequestID'),
        }, status=status.HTTP_201_CREATED)


def complete_payment(payment: Payment):
    """Called by the Daraja callback after a successful STK Push."""
    payment.status = 'completed'
    payment.save(update_fields=['status'])

    if hasattr(payment, 'subscription'):
        payment.subscription.activate()
    elif payment.course:
        Enrollment.objects.get_or_create(learner=payment.learner, course=payment.course)


class MpesaCallbackView(APIView):
    """Daraja posts the STK Push result here asynchronously. Daraja never
    authenticates as a Learner, so this bypasses normal API auth entirely
    and instead trusts a matching, previously-issued CheckoutRequestID."""
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        body = request.data.get('Body', {}).get('stkCallback', {})
        checkout_request_id = body.get('CheckoutRequestID')
        result_code = body.get('ResultCode')

        try:
            payment = Payment.objects.get(provider_reference=checkout_request_id)
        except Payment.DoesNotExist:
            return Response(status=status.HTTP_200_OK)

        if result_code == 0:
            items = {i['Name']: i.get('Value') for i in body.get('CallbackMetadata', {}).get('Item', [])}
            payment.transaction_id = str(items.get('MpesaReceiptNumber', ''))
            payment.save(update_fields=['transaction_id'])
            complete_payment(payment)
        else:
            payment.status = 'failed'
            payment.save(update_fields=['status'])
            if hasattr(payment, 'subscription'):
                payment.subscription.status = 'failed'
                payment.subscription.save(update_fields=['status'])

        return Response(status=status.HTTP_200_OK)


class PaymentHistoryView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(learner=self.request.user)


class PaymentDetailView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(learner=self.request.user)
