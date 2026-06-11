from django.urls import path
from .views import (
    CategoryListView, CourseListView, CourseDetailView,
    EnrollView, MyEnrollmentsView, LessonDetailView, MarkLessonCompleteView,
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('', CourseListView.as_view(), name='course-list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('<int:course_id>/enroll/', EnrollView.as_view(), name='course-enroll'),
    path('my-enrollments/', MyEnrollmentsView.as_view(), name='my-enrollments'),
    path('lessons/<int:lesson_id>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('lessons/<int:lesson_id>/complete/', MarkLessonCompleteView.as_view(), name='lesson-complete'),
]
