# Generated by Django 4.1 on 2023-06-27 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0021_remove_answer_module_answer_question"),
    ]

    operations = [
        migrations.RenameField(
            model_name="answer",
            old_name="question",
            new_name="query",
        ),
    ]
