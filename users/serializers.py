from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Learner


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Learner
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return Learner.objects.create_user(**validated_data)


class LearnerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Learner
        fields = [
            'id', 'email', 'first_name', 'last_name', 'phone_number',
            'date_of_birth', 'profile_picture', 'bio', 'date_joined',
        ]
        read_only_fields = ['id', 'email', 'date_joined']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({'new_password': 'Passwords do not match.'})
        return attrs
