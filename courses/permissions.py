from rest_framework.permissions import BasePermission
from .access import has_course_access


class HasCourseAccess(BasePermission):
    """Grants access if actively enrolled in the course, or holding an
    active all-access subscription."""

    def has_object_permission(self, request, view, obj):
        course = getattr(obj, 'course', obj)
        return has_course_access(request.user, course)
