from django.urls import path
from lessons.apps import LessonsConfig
from lessons.views import lesson


app_name = LessonsConfig.name
urlpatterns = [
    path('lessons/', lesson.LessonListView.as_view(), name='lesson-list'),
    path('lessons/create/', lesson.LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>', lesson.LessonRetrieveView.as_view(), name='lesson-detail'),
    path('lessons/<int:pk>/update/', lesson.LessonUpdateView.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/delete/', lesson.LessonDeleteView.as_view(), name='lesson-delete'),
]