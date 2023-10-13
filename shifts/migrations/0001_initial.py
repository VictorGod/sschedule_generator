# Generated by Django 4.2.6 on 2023-10-13 15:11

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Shift",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_time", models.TimeField(verbose_name="Начало работы")),
                ("end_time", models.TimeField(verbose_name="Окончание работы")),
            ],
        ),
    ]
