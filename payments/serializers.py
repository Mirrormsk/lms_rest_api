from rest_framework import serializers

from lessons.models import Lesson, Course
from payments.models import Payment
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
        fields = "__all__"

