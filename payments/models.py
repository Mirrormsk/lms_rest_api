from django.db import models

from users.models import NULLABLE


class Payment(models.Model):
    METHOD_CASH = 'cash'
    METHOD_TRANSFER_TO_ACCOUNT = 'account'

    METHODS = (
        (METHOD_CASH, 'Наличные'),
        (METHOD_TRANSFER_TO_ACCOUNT, 'Перевод на счет'),
    )

    user = models.ForeignKey('users.User', on_delete=models.DO_NOTHING, verbose_name='студент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата и время')
    course = models.ForeignKey('lessons.Course', on_delete=models.PROTECT, **NULLABLE)
    lesson = models.ForeignKey('lessons.Lesson', on_delete=models.PROTECT, **NULLABLE)
    amount = models.PositiveIntegerField(verbose_name='сумма')
    method = models.CharField(max_length=30, choices=METHODS, verbose_name='метод')

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'

    def __str__(self):
        return f"{self.created_at}: {self.user.email}, {self.amount}"
