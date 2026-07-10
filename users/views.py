from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import LearnerProfileSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = LearnerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
