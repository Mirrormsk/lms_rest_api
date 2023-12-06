from rest_framework import viewsets
from lessons.serializers.lesson import CourseSerializer
from lessons.models import Course


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet from Course model
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
