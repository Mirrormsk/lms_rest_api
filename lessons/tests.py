from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APITransactionTestCase

from lessons.models import Lesson
from users.models import User


class LessonsTestCase(APITransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.lesson_create_url = reverse("lessons:lesson-create")
        self.user1 = User.objects.create(email="test@test.com", password="Password1234")
        self.lesson = Lesson.objects.create(
            title="Lesson 1", description="Lesson 1", owner=self.user1
        )
        self.lesson2 = Lesson.objects.create(
            title="Lesson 2", description="Lesson 2", owner=None
        )

    def tearDown(self):
        # Очистит базу данных после теста и сбросьте счетчик id
        Lesson.objects.all().delete()


    def test_get_lessons_list(self):
        """Тест вывода списка уроков"""
        print("Вызов test_get_lessons_list")
        self.client.force_authenticate(user=self.user1)
        response = self.client.get("/lessons/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 1,
                        "in_courses": [],
                        "title": "Lesson 1",
                        "description": "Lesson 1",
                        "preview": None,
                        "video_url": None,
                        "owner": 1,
                    }
                ],
            },
        )

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.user1)
        new_lesson_data = {"title": "Lesson New", "description": "Lesson New"}
        response = self.client.post(self.lesson_create_url, new_lesson_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(new_lesson_data, response.json())
