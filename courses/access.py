from django.utils import timezone
from .models import Enrollment


def has_course_access(user, course):
    """True if the learner is actively enrolled in this course, or holds
    an active all-access subscription."""
    if not user.is_authenticated:
        return False
    if Enrollment.objects.filter(learner=user, course=course, status='active').exists():
        return True
    from payments.models import Subscription
    return Subscription.objects.filter(
        learner=user, status='active', expires_at__gt=timezone.now()
    ).exists()
