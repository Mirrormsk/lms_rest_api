from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from lessons.models import Lesson
from lessons.paginators import LessonPagination
from lessons.permissions import IsModerator, IsOwner
from lessons.serializers.lesson import LessonSerializer
from lessons.services import user_in_group


class LessonListView(generics.ListAPIView):

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LessonPagination

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Lesson.objects.none()

        if user_in_group(user, group_name="moderators"):
            return Lesson.objects.prefetch_related("course_set").all()

        return Lesson.objects.prefetch_related("course_set").filter(owner=user)


class LessonCreateView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonUpdateView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class LessonDeleteView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]
