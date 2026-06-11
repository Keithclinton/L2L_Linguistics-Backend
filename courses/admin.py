from django.contrib import admin
from .models import Category, Course, Lesson, Enrollment, LessonProgress


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ['title', 'order', 'duration_minutes', 'is_preview', 'video_url']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'level', 'price', 'is_free', 'is_published', 'created_at']
    list_filter = ['is_published', 'level', 'category']
    search_fields = ['title', 'description']
    list_editable = ['is_published']
    inlines = [LessonInline]

    @admin.display(boolean=True)
    def is_free(self, obj):
        return obj.is_free


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'duration_minutes', 'is_preview']
    list_filter = ['course', 'is_preview']
    search_fields = ['title', 'course__title']
    ordering = ['course', 'order']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['learner', 'course', 'status', 'enrolled_at']
    list_filter = ['status', 'enrolled_at']
    search_fields = ['learner__email', 'course__title']
    raw_id_fields = ['learner', 'course']


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'lesson', 'completed', 'completed_at']
    list_filter = ['completed']
