# Generated by Django 3.0.7 on 2020-07-28 00:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("watch", "0004_auto_20200722_1912"),
    ]

    operations = [
        migrations.AddField(
            model_name="score",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                help_text="Date and time the score was saved.",
            ),
            preserve_default=False,
        ),
    ]
