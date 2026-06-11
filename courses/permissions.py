from rest_framework.permissions import BasePermission
from .models import Enrollment


class IsEnrolled(BasePermission):
    """Grants access only if the learner is actively enrolled in the course."""

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        course = getattr(obj, 'course', obj)
        return Enrollment.objects.filter(
            learner=request.user, course=course, status='active'
        ).exists()
