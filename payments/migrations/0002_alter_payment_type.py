# Generated by Django 5.0 on 2023-12-08 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="type",
            field=models.CharField(
                choices=[("cash", "Наличные"), ("started", "Перевод на счет")],
                max_length=30,
                verbose_name="тип",
            ),
        ),
    ]
