# Generated by Django 5.0 on 2023-12-21 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lessons", "0006_rename_subscribe_subscription"),
    ]

    operations = [
        migrations.AddField(
            model_name="lesson",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="обновлен"),
        ),
    ]
