import random

from django.core.management.base import BaseCommand

from lessons.models import Course, Lesson
from payments.models import Payment
from users.models import User


class Command(BaseCommand):
    help = (
        "Create sample payments data. "
        "Takes optional positional argument - count of payments"
    )

    @staticmethod
    def generate_amount():
        return random.randint(1_000, 200_000)

    def add_arguments(self, parser):
        parser.add_argument(
            "count",
            nargs="?",
            type=int,
            help="How many payments need to create (optional, default = 10)",
            default=10,
        )

    def handle(self, *args, **options):
        count = options["count"]

        users = User.objects.all()
        courses = Course.objects.all()
        lessons = Lesson.objects.all()

        for _ in range(count):
            product_choice = random.choice(
                [{"course": random.choice(courses)}, {"lesson": random.choice(lessons)}]
            )
            payment = Payment(
                user=random.choice(users),
                amount=self.generate_amount(),
                type=random.choice(Payment.TYPES),
                **product_choice,
            )
            payment.save()

        message = f"Successful generated {count} payments."

        self.stdout.write(self.style.SUCCESS(message))
