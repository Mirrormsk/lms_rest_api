from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from lessons.serializers.course import CourseSerializer
from lessons.models import Course, Lesson
from lessons.permissions import IsModerator, IsOwner
from lessons.services import user_in_group


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Course model
    """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Course.objects.none()

        if user_in_group(user, 'moderators'):
            return Course.objects.all()

        return Course.objects.filter(owner=user)

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
                permission_classes = [IsAuthenticated, IsOwner | IsModerator]
            case "create":
                permission_classes = [IsAuthenticated, ~IsModerator]
            case "update" | "partial_update":
                permission_classes = [IsAuthenticated, IsOwner | IsModerator]
            case "destroy":
                permission_classes = [IsAuthenticated, IsOwner]
            case _:
                permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
