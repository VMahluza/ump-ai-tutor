# Generated by Django 4.1 on 2023-06-25 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0009_registration_level"),
    ]

    operations = [
        migrations.AlterField(
            model_name="registration",
            name="level",
            field=models.CharField(
                choices=[("First Year", "1")], default="First Year", max_length=50
            ),
        ),
    ]
