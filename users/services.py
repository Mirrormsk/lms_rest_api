import datetime

from users.models import User


def deactivate_inactive_users(inactivity_threshold=30) -> None:
    """
    Deactivates users who have been inactive for more than the specified threshold.
    :param inactivity_threshold: Inactivity threshold in days (default is 30 days).
    """
    now = datetime.datetime.now(datetime.UTC)
    inactive_cutoff_date = now - datetime.timedelta(days=inactivity_threshold)

    inactive_users = User.objects.filter(is_active=True, last_login__lt=inactive_cutoff_date)
    inactive_users.update(is_active=False)
