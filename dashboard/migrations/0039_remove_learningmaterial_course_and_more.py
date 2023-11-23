# Generated by Django 4.1 on 2023-11-23 00:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0038_alter_module_course"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="learningmaterial",
            name="course",
        ),
        migrations.AddField(
            model_name="learningmaterial",
            name="module",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="module_learning_materials",
                to="dashboard.course",
            ),
        ),
        migrations.AlterField(
            model_name="query",
            name="course",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="course_queries",
                to="dashboard.course",
            ),
        ),
        migrations.AlterField(
            model_name="query",
            name="module",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="module_queries",
                to="dashboard.module",
            ),
        ),
        migrations.AlterField(
            model_name="query",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_queries",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
