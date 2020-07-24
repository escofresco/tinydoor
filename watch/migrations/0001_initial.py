# Generated by Django 3.0.7 on 2020-07-08 15:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Score",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "video_link",
                    models.CharField(
                        blank=True,
                        help_text="Link to the video being scored (can play it back later).",
                        max_length=200,
                        null=True,
                    ),
                ),
                (
                    "emotion_score",
                    models.FloatField(
                        help_text="Tinydoor score for gauging positive customer experience."
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="User who posted the video being scored.",
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
