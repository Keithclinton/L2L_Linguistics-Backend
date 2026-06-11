from rest_framework import serializers
from .models import Category, Course, Lesson, Enrollment, LessonProgress


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'video_url', 'order', 'duration_minutes', 'is_preview']


class LessonListSerializer(serializers.ModelSerializer):
    """Slim serializer for lesson lists — omits content body."""
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'order', 'duration_minutes', 'is_preview']


class CourseListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'category', 'thumbnail',
            'level', 'price', 'is_free', 'lesson_count', 'created_at',
        ]

    def get_lesson_count(self, obj):
        return obj.lessons.count()


class CourseDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    lessons = serializers.SerializerMethodField()
    lesson_count = serializers.SerializerMethodField()
    is_enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'category', 'thumbnail', 'level',
            'price', 'is_free', 'lesson_count', 'lessons', 'is_enrolled', 'created_at',
        ]

    def get_lessons(self, obj):
        request = self.context.get('request')
        lessons = obj.lessons.all()
        # Show full lesson list only to enrolled learners; others see preview lessons only
        if request and request.user.is_authenticated:
            enrolled = obj.enrollments.filter(learner=request.user, status='active').exists()
            if enrolled:
                return LessonListSerializer(lessons, many=True).data
        return LessonListSerializer(lessons.filter(is_preview=True), many=True).data

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.enrollments.filter(learner=request.user, status='active').exists()
        return False


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'status', 'enrolled_at', 'completed_at']


class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ['id', 'lesson', 'completed', 'completed_at']
