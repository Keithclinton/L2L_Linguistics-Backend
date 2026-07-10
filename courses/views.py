from django.utils import timezone
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny

from .models import Category, Course, Lesson, Enrollment, LessonProgress
from .serializers import (
    CategorySerializer, CourseListSerializer, CourseDetailSerializer,
    LessonSerializer, EnrollmentSerializer, LessonProgressSerializer,
)
from .access import has_course_access


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class CourseListView(generics.ListAPIView):
    serializer_class = CourseListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Course.objects.filter(is_published=True).select_related('category')
        category = self.request.query_params.get('category')
        level = self.request.query_params.get('level')
        free = self.request.query_params.get('free')
        if category:
            qs = qs.filter(category__name__icontains=category)
        if level:
            qs = qs.filter(level=level)
        if free == 'true':
            qs = qs.filter(price=0)
        elif free == 'false':
            qs = qs.exclude(price=0)
        return qs


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.filter(is_published=True).select_related('category')
    serializer_class = CourseDetailSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class EnrollView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id, is_published=True)
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

        if has_course_access(request.user, course):
            return Response({'detail': 'Already enrolled.'}, status=status.HTTP_400_BAD_REQUEST)

        if not course.is_free:
            return Response(
                {'detail': 'This is a paid course. Please complete payment to enroll.'},
                status=status.HTTP_402_PAYMENT_REQUIRED,
            )

        enrollment = Enrollment.objects.create(learner=request.user, course=course)
        return Response(EnrollmentSerializer(enrollment).data, status=status.HTTP_201_CREATED)


class MyEnrollmentsView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(
            learner=self.request.user
        ).select_related('course', 'course__category')


class LessonDetailView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        lesson = generics.get_object_or_404(Lesson, pk=self.kwargs['lesson_id'])
        if lesson.is_preview:
            return lesson
        if not has_course_access(self.request.user, lesson.course):
            self.permission_denied(self.request, message='Enrollment or an active subscription is required to access this lesson.')
        return lesson


class MarkLessonCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, lesson_id):
        lesson = generics.get_object_or_404(Lesson, pk=lesson_id)
        if not has_course_access(request.user, lesson.course):
            return Response({'detail': 'Not enrolled in this course.'}, status=status.HTTP_403_FORBIDDEN)

        enrollment, _ = Enrollment.objects.get_or_create(learner=request.user, course=lesson.course)
        progress, created = LessonProgress.objects.get_or_create(
            enrollment=enrollment, lesson=lesson
        )
        if not progress.completed:
            progress.completed = True
            progress.completed_at = timezone.now()
            progress.save()

        return Response(LessonProgressSerializer(progress).data)
