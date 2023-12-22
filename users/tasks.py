from celery import shared_task
from users.services import deactivate_inactive_users


@shared_task
def deactivate_inactive_users_task() -> None:
    deactivate_inactive_users()
