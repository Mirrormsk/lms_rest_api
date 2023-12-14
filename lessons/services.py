from django.contrib.auth.models import User


def user_in_group(user: User, group_name: str) -> bool:
    return user.groups.filter(name=group_name).exists()
