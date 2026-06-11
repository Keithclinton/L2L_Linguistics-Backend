from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from courses.models import Course, Enrollment
from .models import Payment
from .serializers import PaymentInitiateSerializer, PaymentSerializer


class InitiatePaymentView(APIView):
    """
    Placeholder for payment initiation.
    Wire up M-Pesa STK Push or Stripe PaymentIntent here when ready.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PaymentInitiateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course_id = serializer.validated_data['course_id']
        try:
            course = Course.objects.get(pk=course_id, is_published=True)
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

        if course.is_free:
            return Response({'detail': 'This course is free. Use the enroll endpoint.'}, status=status.HTTP_400_BAD_REQUEST)

        if Enrollment.objects.filter(learner=request.user, course=course, status='active').exists():
            return Response({'detail': 'Already enrolled.'}, status=status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.create(
            learner=request.user,
            course=course,
            amount=course.price,
            currency='KES',
            provider='manual',
            status='pending',
            phone_number=serializer.validated_data.get('phone_number', ''),
        )

        # TODO: Integrate payment provider here (M-Pesa / Stripe)
        # On successful provider confirmation, call _complete_payment(payment)

        return Response({
            'detail': 'Payment initiated. Integration pending.',
            'payment_id': payment.id,
            'amount': str(payment.amount),
            'currency': payment.currency,
        }, status=status.HTTP_201_CREATED)


def complete_payment(payment: Payment):
    """Called by provider webhook after successful payment."""
    payment.status = 'completed'
    payment.save()
    Enrollment.objects.get_or_create(learner=payment.learner, course=payment.course)


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
