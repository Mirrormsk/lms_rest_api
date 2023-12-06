from django.db import models
from users.models import NULLABLE


class Lesson(models.Model):

    title = models.CharField(max_length=255, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='lessons', verbose_name='превью', **NULLABLE)
    video_url = models.URLField(verbose_name='ссылка на видео', **NULLABLE)

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='lessons', verbose_name='превью', **NULLABLE)
    lessons = models.ManyToManyField(Lesson)

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def __str__(self):
        return self.title
