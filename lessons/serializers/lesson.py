from rest_framework import serializers
from lessons.models import Lesson
from lessons.serializers.course import CourseSerializer


class LessonSerializer(serializers.ModelSerializer):
    in_courses = CourseSerializer(many=True, read_only=True, source='course_set')

    class Meta:
        model = Lesson
        fields = '__all__'

