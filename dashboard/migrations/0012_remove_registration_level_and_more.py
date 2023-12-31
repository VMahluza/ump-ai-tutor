# Generated by Django 4.1 on 2023-06-25 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0011_alter_registration_level"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="registration",
            name="level",
        ),
        migrations.AddField(
            model_name="registration",
            name="level_of_study",
            field=models.CharField(
                choices=[
                    ("1", "First Year"),
                    ("2", "Second Year"),
                    ("3", "Third Year"),
                    ("4", "4th Year"),
                ],
                default="1",
                max_length=50,
            ),
        ),
    ]
