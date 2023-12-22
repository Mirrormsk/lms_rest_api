from rest_framework import serializers

from lessons.models import Course, Lesson, Subscription
from lessons.validators import AllowedLinksValidator


class LessonInCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):

    lessons_count = serializers.IntegerField(read_only=True, source="lessons.count")
    lessons = LessonInCourseSerializer(many=True, read_only=True)
    is_subscribe_active = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "owner",
            "lessons_count",
            "title",
            "description",
            "preview",
            "lessons",
            "is_subscribe_active",
            "updated_at",
        )
        validators = [AllowedLinksValidator(field="description")]

    def get_is_subscribe_active(self, instance):
        user = self.context["request"].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=instance, is_active=True).exists()
        return False
