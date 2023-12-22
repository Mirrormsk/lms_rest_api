import logging
import datetime
from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import QuerySet

from lessons.models import Subscription, Course

logger = logging.getLogger(__name__)


def user_in_group(user: User, group_name: str) -> bool:
    return user.groups.filter(name=group_name).exists()


def send_course_updated_email(course: Course, email: str) -> None:

    subject = f"You have new updates for {course.title}"
    message = f"Course {course.title} was updated. Please check the details below."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    try:
        send_mail(
            subject=subject,
            from_email=from_email,
            message=message,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        print("email sent")
    except SMTPException as ex:
        logger.exception(f"Error sending mail to {email}: {ex}")


def get_subscribers_emails_from_course(course: Course) -> QuerySet:
    subscribers: QuerySet = Subscription.objects.filter(course=course, is_active=True)

    if not subscribers.exists():
        return None

    subscriber_emails = (
        subscribers
        .select_related("user")
        .values_list("user__email", flat=True)
    ).distinct()

    return subscriber_emails


def inform_subscribers_about_update(course_id: int) -> None:
    course: Course = Course.objects.get(id=course_id)
    subscriber_emails = get_subscribers_emails_from_course(course)
    for email in subscriber_emails:
        send_course_updated_email(course, email)
