from django.db import models
from users.models import NULLABLE


class Lesson(models.Model):

    title = models.CharField(max_length=255, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    preview = models.ImageField(upload_to="lessons", verbose_name="превью", **NULLABLE)
    video_url = models.URLField(verbose_name="ссылка на видео", **NULLABLE)
    owner = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, **NULLABLE, verbose_name="Создал"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="обновлен")

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = ("pk",)

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    preview = models.ImageField(upload_to="lessons", verbose_name="превью", **NULLABLE)
    lessons = models.ManyToManyField(Lesson)
    owner = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, **NULLABLE, verbose_name="Создал"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="обновлен")

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering = ("pk",)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, verbose_name="активна")

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"

    def __str__(self):
        return f"Subscription to {self.course} for {self.user}"
