# Generated by Django 4.1 on 2023-11-22 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0033_rename_notifications_notification"),
    ]

    operations = [
        migrations.RenameField(
            model_name="notification",
            old_name="date_time",
            new_name="date_made",
        ),
    ]
