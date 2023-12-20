from payments.models import Payment
from rest_framework import serializers


def has_lesson_xor_course_validator(value):
    payment: dict = dict(value)
    if not (payment['lesson'] is not None) ^ (payment['course'] is not None):
        raise serializers.ValidationError("Choose one of lesson or course")
