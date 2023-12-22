from celery import shared_task

from lessons.services import inform_subscribers_about_update


@shared_task
def inform_subscribers_about_update_task(course_id: int):
    inform_subscribers_about_update(course_id)
