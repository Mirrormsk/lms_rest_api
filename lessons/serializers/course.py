from rest_framework import serializers

from lessons.models import Course


class CourseSerializer(serializers.ModelSerializer):

    lessons_count = serializers.IntegerField(read_only=True, source='lessons.count')

    class Meta:
        model = Course
        fields = '__all__'
