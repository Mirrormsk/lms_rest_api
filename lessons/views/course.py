from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from lessons.serializers.course import CourseSerializer
from lessons.models import Course, Lesson
from lessons.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Course model
    """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    @action(detail=True, methods=["post"])
    def add_lesson(self, request, pk=None):
        course = self.get_object()
        lesson_id = request.data.get("lesson_id")

        if lesson_id and lesson_id in Lesson.objects.values_list("pk", flat=True):

            lesson = Lesson.objects.get(pk=lesson_id)
            course.lessons.add(lesson)

            course.lessons_count = course.lessons.count()
            course.save()

            serializer = self.get_serializer(course)
            return Response(serializer.data)

        return Response({"detail": "Invalid lesson ID"}, status=400)

    def get_permissions(self):
        match self.action:
            case "list" | "retrieve":
                permission_classes = [IsAuthenticated]
            case "create":
                permission_classes = [IsAuthenticated, ~IsModerator]
            case "update" | "partial_update":
                permission_classes = [IsAuthenticated, IsOwner | IsModerator]
            case "destroy":
                permission_classes = [IsAuthenticated, IsOwner]
            case _:
                permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
