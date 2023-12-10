from rest_framework import serializers

from lessons.models import Course, Lesson


class LessonInCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):

    lessons_count = serializers.IntegerField(read_only=True, source="lessons.count")
    lessons = LessonInCourseSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ("id", "lessons_count", "title", "description", "preview", "lessons")
