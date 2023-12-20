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
    is_paid = models.BooleanField(default=False, verbose_name='оплачен')
    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'

    def __str__(self):
        return f"{self.created_at}: {self.user.email}, {self.amount}"


class PaymentSession(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='session')
    session_id = models.CharField(max_length=255, unique=True, verbose_name='session id')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='создана')

    class Meta:
        verbose_name = 'платежная сессия'
        verbose_name_plural = 'платежные сессии'
        unique_together = ('payment', 'session_id')
        ordering = ('-created_at', "payment")

    def __str__(self):
        return f"{self.session_id}"
