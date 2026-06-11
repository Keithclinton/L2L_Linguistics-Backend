from rest_framework import serializers
from .models import Payment


class PaymentInitiateSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    phone_number = serializers.CharField(max_length=20, required=False)


class PaymentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'course', 'course_title', 'amount', 'currency',
            'provider', 'status', 'transaction_id', 'created_at',
        ]
        read_only_fields = fields
