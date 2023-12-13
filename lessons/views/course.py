from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from lessons.serializers.course import CourseSerializer
from lessons.models import Course, Lesson


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet from Course model
    """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def add_lesson(self, request, pk=None):
        course = self.get_object()
        lesson_id = request.data.get("lesson_id")

        if lesson_id and lesson_id in Lesson.objects.values_list('pk', flat=True):

            lesson = Lesson.objects.get(pk=lesson_id)
            course.lessons.add(lesson)

            course.lessons_count = course.lessons.count()
            course.save()

            serializer = self.get_serializer(course)
            return Response(serializer.data)

        return Response({"detail": "Invalid lesson ID"}, status=400)
