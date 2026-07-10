from rest_framework import serializers
from .models import Payment, Subscription


class PaymentInitiateSerializer(serializers.Serializer):
    course_id = serializers.IntegerField(required=False)
    plan = serializers.ChoiceField(choices=Subscription.PLAN_CHOICES, required=False)
    phone_number = serializers.CharField(max_length=20, required=False)

    def validate(self, attrs):
        if not attrs.get('course_id') and not attrs.get('plan'):
            raise serializers.ValidationError('Provide either course_id or plan.')
        if attrs.get('course_id') and attrs.get('plan'):
            raise serializers.ValidationError('Provide only one of course_id or plan, not both.')
        return attrs


class PaymentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True, default=None)

    class Meta:
        model = Payment
        fields = [
            'id', 'course', 'course_title', 'amount', 'currency',
            'provider', 'status', 'transaction_id', 'created_at',
        ]
        read_only_fields = fields


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'plan', 'status', 'starts_at', 'expires_at', 'created_at']
        read_only_fields = fields
