from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APITransactionTestCase

from lessons.models import Lesson, Course, Subscription
from users.models import User


class LessonsTestCase(APITransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.lesson_create_url = reverse("lessons:lesson-create")
        self.user1 = User.objects.create(email="test@test.com", password="Password1234")
        self.user2 = User.objects.create(
            email="test2@test.com", password="Password1234"
        )
        self.lesson = Lesson.objects.create(
            title="Lesson 1", description="Lesson 1", owner=self.user1
        )
        self.lesson2 = Lesson.objects.create(
            title="Lesson 2", description="Lesson 2", owner=None
        )

    def tearDown(self):
        # Очистит базу данных после теста и сбросьте счетчик id
        Lesson.objects.all().delete()

    def test_1_get_lessons_list(self):
        """Тест вывода списка уроков"""
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

    def test_2_create_lesson(self):
        self.client.force_authenticate(user=self.user1)
        new_lesson_data = {"title": "Lesson New", "description": "Lesson New"}
        response = self.client.post(self.lesson_create_url, new_lesson_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_3_delete_lesson(self):
        self.client.force_authenticate(user=self.user1)

        # Creating new lesson
        new_lesson_data = {"title": "Lesson New", "description": "Lesson New"}
        response = self.client.post(self.lesson_create_url, new_lesson_data)
        new_lesson_id = response.data["id"]

        # Try to get by owner
        try_to_get_created_lesson = self.client.get(
            reverse("lessons:lesson-detail", args=[new_lesson_id])
        )
        self.assertEqual(try_to_get_created_lesson.status_code, status.HTTP_200_OK)

        # The user cannot delete someone else's own lesson
        self.client.force_authenticate(user=self.user2)
        delete_response = self.client.delete(
            reverse("lessons:lesson-delete", args=[new_lesson_id])
        )
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)

        # Owner can delete lesson
        self.client.force_authenticate(user=self.user1)
        self.client.delete(reverse("lessons:lesson-delete", args=[new_lesson_id]))

        # Check that lesson was deleted
        try_to_get_deleted_lesson = self.client.get(
            reverse("lessons:lesson-detail", args=[new_lesson_id])
        )
        self.assertEqual(
            try_to_get_deleted_lesson.status_code, status.HTTP_404_NOT_FOUND
        )

    def test_4_update_lesson(self):
        self.client.force_authenticate(user=self.user1)

        # Creating new lesson
        new_lesson_data = {"title": "Lesson New", "description": "Lesson New"}
        response = self.client.post(self.lesson_create_url, new_lesson_data)
        new_lesson_id = response.data["id"]

        # The user cannot update someone else's own lesson
        self.client.force_authenticate(user=self.user2)
        try_to_update_created_lesson = self.client.patch(
            reverse("lessons:lesson-update", args=[new_lesson_id]),
            data={"description": "Updated lesson description"},
        )
        self.assertEqual(
            try_to_update_created_lesson.status_code, status.HTTP_403_FORBIDDEN
        )

        # Owner can update lesson
        self.client.force_authenticate(user=self.user1)
        try_to_update_created_lesson = self.client.patch(
            reverse("lessons:lesson-update", args=[new_lesson_id]),
            data={"description": "Updated lesson description"},
        )
        self.assertEqual(try_to_update_created_lesson.status_code, status.HTTP_200_OK)
        self.assertEqual(
            try_to_update_created_lesson.data["description"],
            "Updated lesson description",
        )

    def test_5_lesson_detail(self):
        self.client.force_authenticate(user=self.user1)
        lesson_data_response = self.client.get(
            reverse("lessons:lesson-detail", args=[1])
        )
        self.assertEqual(lesson_data_response.status_code, status.HTTP_200_OK)
        self.assertEqual(lesson_data_response.data["title"], "Lesson 1")


class SubscriptionTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(email="test@test.com", password="Password1234")
        self.course1 = Course.objects.create(
            title="Test course", description="Test course description"
        )

    def test_1_add_subscription(self):
        self.client.force_authenticate(user=self.user1)
        data = {"user": self.user1.id, "course": self.course1.id}
        new_subscription_response = self.client.post(
            reverse("lessons:subscription-create"), data=data
        )
        self.assertEqual(new_subscription_response.status_code, status.HTTP_201_CREATED)

    def test_2_destroy_subscription(self):
        self.client.force_authenticate(user=self.user1)

        data = {"user": self.user1.id, "course": self.course1.id}
        new_subscription_response = self.client.post(
            reverse("lessons:subscription-create"), data=data
        )
        new_subscription_id = new_subscription_response.data["id"]
        deleted_subscription_response = self.client.delete(
            reverse("lessons:subscription-delete", args=[new_subscription_id])
        )
        self.assertEqual(deleted_subscription_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Subscription.objects.filter(is_active=True)), 0)
