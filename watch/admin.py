from django.contrib import admin

from .models import Score


class ScoreAdmin(admin.ModelAdmin):
    fields = [
        'user',
        'task_id',
        'emotion_score',
        'created'
    ]

admin.site.register(Score, ScoreAdmin)
