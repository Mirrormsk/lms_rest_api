from rest_framework import serializers

from lessons.models import Lesson, Course
from payments.models import Payment
from payments.validators import has_lesson_xor_course_validator
from users.models import User


class PaymentSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField("email", queryset=User.objects.all())
    lesson = serializers.SlugRelatedField("title", queryset=Lesson.objects.all())
    course = serializers.SlugRelatedField("title", queryset=Course.objects.all())
    method = serializers.CharField(source="get_method_display")

    class Meta:
        model = Payment
        fields = "__all__"


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('user', 'method', 'lesson', 'course', 'amount')
        validators = [has_lesson_xor_course_validator]


class PaymentCheckStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('pk',)
