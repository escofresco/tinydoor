# from django.db import models

# from tinydoor.users.models import User


"""
class Score(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        help_text="User who posted the video being scored."
    )
    video_link = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text=("Link to the video " + "being scored (can play it back later)."),
    )
    emotion_score = models.FloatField(
        help_text=("Tinydoor score for gauging positive customer experience.")
    )

    def __str__(self):
        '''Return a string representation of the Score.'''
        return f"Score for {self.user}, on Video {self.video_link}"

    def get_absolute_url(self):
        '''Return a fully qualified path to the Score, to view it later.'''
    """
