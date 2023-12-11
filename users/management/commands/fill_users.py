import string

from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from django.utils.crypto import get_random_string
import random

from users.models import User


class Command(BaseCommand):
    @staticmethod
    def randomstring(length):
        """Generate random string"""
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for i in range(length))

    def generate_email(self):
        """Generate random email"""
        login = self.randomstring(8)
        domain = self.randomstring(5)
        return f"{login}@{domain}.com"

    def add_arguments(self, parser):
        parser.add_argument(
            "count",
            nargs="?",
            type=int,
            help="How many users need to create (optional, default = 10)",
            default=10,
        )

    def handle(self, *args, **options):
        count = options["count"]
        try:
            for _ in range(count):

                user = User.objects.create(
                    email=self.generate_email(),
                    first_name=self.randomstring(10).title(),
                    last_name=self.randomstring(10).title(),
                    is_staff=False,
                    password=self.randomstring(10)
                )

        except Exception as ex:
            self.stdout.write(self.style.ERROR(f"Error: {ex}"))

        else:
            success_message = (
                f"Successful created {count} users.\n"
                f"Now you can generate sample payments with command:\n"
                f"python3 manage.py fill_payments <count>"
            )
            self.stdout.write(self.style.SUCCESS(success_message))
