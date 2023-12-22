run-celery:
	poetry run celery -A config worker -l INFO

run-celery-beat:
	poetry run celery -A config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

run-celery-and-beat:
	poetry run celery -A config worker -l INFO & poetry run celery -A config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
