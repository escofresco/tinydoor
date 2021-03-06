# Generated by Django 3.0.7 on 2020-07-22 15:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("watch", "0002_auto_20200722_1517"),
    ]

    operations = [
        migrations.AlterField(
            model_name="score",
            name="user",
            field=models.ForeignKey(
                help_text="User who posted the video being scored.",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
