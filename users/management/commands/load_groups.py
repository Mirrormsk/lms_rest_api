from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from users.models import User


class Command(BaseCommand):
    help = "Create groups"

    def handle(self, *args, **options):

        moderators, moderators_created = Group.objects.get_or_create(name="moderators")

        if moderators_created:
            message = "Moderators group were successfully created."
        else:
            message = "Moderators group already exists."
        self.stdout.write(self.style.SUCCESS(message))

        moderator_email = "moderator@sample.ru"
        moderator_psw = get_random_string(length=8)

        try:
            moderator,_ = User.objects.get_or_create(
                email=moderator_email,
                first_name="Moderator",
                last_name="Sample",
                is_staff=False,
            )

            moderator.set_password(moderator_psw)
            moderator.groups.add(moderators)
            moderator.save()

        except Exception as ex:
            self.stdout.write(self.style.ERROR(f"Error: {ex}"))

        else:
            success_message = (f"Successful created sample staff:\n"
                               f"Moderator: {moderator_email}, password: {moderator_psw}")

            self.stdout.write(self.style.SUCCESS(success_message))

