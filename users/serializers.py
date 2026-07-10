from rest_framework import serializers
from .models import Learner


class LearnerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Learner
        fields = [
            'id', 'email', 'first_name', 'last_name', 'phone_number',
            'date_of_birth', 'profile_picture', 'bio', 'date_joined',
        ]
        read_only_fields = ['id', 'email', 'date_joined']
