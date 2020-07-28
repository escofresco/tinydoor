from django.db import models

from tinydoor.users.models import User


class Score(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        help_text="User who posted the video being scored.",
        null=True,
    )
    task_id = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text=("Link to the Celery task that " + "scored the video."),
    )
    emotion_score = models.FloatField(
        help_text=("Tinydoor score for gauging positive customer experience."),
        blank=True,
        null=True,
    )
    created = models.DateTimeField("Date and time the score was saved.")

    def __str__(self):
        """Return a string representation of the Score."""
        return f"Score for {self.user}, on Task {self.task_id}"

    def get_absolute_url(self):
        """Return a fully qualified path to the Score, to view it later."""
