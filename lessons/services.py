import logging
from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail

from lessons.models import Lesson

logger = logging.getLogger(__name__)


def user_in_group(user: User, group_name: str) -> bool:
    return user.groups.filter(name=group_name).exists()


def send_lesson_updated_email(lesson: Lesson, user: User):
    user_email = user.email

    subject = f"You have new updates for {lesson.title}"
    message = f"Lesson {lesson.title} was updated. Please check the details below."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    try:
        send_mail(
            subject=subject,
            from_email=from_email,
            message=message,
            recipient_list=recipient_list,
            fail_silently=False,
        )
    except SMTPException as ex:
        logger.exception(f"Error sending mail to {user_email}: {ex}")
