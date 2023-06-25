# Generated by Django 4.1 on 2023-06-25 11:27

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0002_user_auth_key"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="auth_key",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MaxValueValidator(9999999999),
                    django.core.validators.MinValueValidator(1000000000),
                ],
            ),
        ),
        migrations.CreateModel(
            name="AuthKeys",
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
                (
                    "role",
                    models.CharField(
                        blank=True,
                        choices=[("LECTURE", "LECTURE"), ("TUTOR", "TUTOR")],
                        max_length=50,
                    ),
                ),
                (
                    "auth_key",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MaxValueValidator(9999999999),
                            django.core.validators.MinValueValidator(1000000000),
                        ],
                    ),
                ),
                ("available", models.BooleanField(default=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
