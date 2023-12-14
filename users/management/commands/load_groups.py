from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create groups"

    def handle(self, *args, **options):

        moderators, moderators_created = Group.objects.get_or_create(name="moderators")

        if moderators_created:
            message = (
                "Moderators group were successfully created."
            )
        else:
            message = "Moderators group already exists."
        self.stdout.write(self.style.SUCCESS(message))
