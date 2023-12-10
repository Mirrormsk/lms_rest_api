from rest_framework import serializers
from lessons.models import Lesson, Course


class CourseNameOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title']


class LessonSerializer(serializers.ModelSerializer):
    in_courses = CourseNameOnlySerializer(many=True, read_only=True, source='course_set')

    class Meta:
        model = Lesson
        fields = '__all__'

