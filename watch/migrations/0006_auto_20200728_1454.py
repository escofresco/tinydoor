# Generated by Django 3.0.7 on 2020-07-28 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("watch", "0005_score_created"),
    ]

    operations = [
        migrations.AlterField(
            model_name="score",
            name="created",
            field=models.DateTimeField(
                verbose_name="Date and time the score was saved."
            ),
        ),
    ]
