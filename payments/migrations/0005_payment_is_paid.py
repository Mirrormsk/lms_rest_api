# Generated by Django 5.0 on 2023-12-19 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0004_remove_payment_type_payment_method"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="is_paid",
            field=models.BooleanField(default=False, verbose_name="оплачен"),
        ),
    ]