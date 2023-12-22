import datetime

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from lessons.paginators import CoursePagination
from lessons.serializers.course import CourseSerializer
from lessons.models import Course, Lesson
from lessons.permissions import IsModerator, IsOwner
from lessons.services import user_in_group
from lessons.tasks import inform_subscribers_about_update_task


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Course model
    """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Course.objects.none()

        if user_in_group(user, group_name='moderators'):
            return Course.objects.prefetch_related('lessons').all()

        return Course.objects.prefetch_related('lessons').filter(owner=user)

    @action(detail=True, methods=["post"])
    def add_lesson(self, request, pk=None):
        course = self.get_object()
        lesson_id = request.data.get("lesson_id")

        if user_in_group(request.user, group_name='moderators'):
            lessons = Lesson.objects.all()
        else:
            lessons = Lesson.objects.filter(owner=request.user)

        if lesson_id and lesson_id in lessons.values_list("pk", flat=True):

            lesson = Lesson.objects.get(pk=lesson_id)
            course.lessons.add(lesson)

            course.lessons_count = course.lessons.count()

            serializer = self.get_serializer(course)

            now = datetime.datetime.now(datetime.UTC)
            if now - course.updated_at > datetime.timedelta(hours=4):
                inform_subscribers_about_update_task.delay(course.id)

            course.save()
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
