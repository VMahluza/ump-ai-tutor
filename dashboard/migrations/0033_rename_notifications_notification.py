# Generated by Django 4.1 on 2023-11-22 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0032_alter_module_description_notifications"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Notifications",
            new_name="Notification",
        ),
    ]