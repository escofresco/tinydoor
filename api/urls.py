from api.views import ScoreData
from django.urls import path

urlpatterns = [
    path("score-data/", ScoreData.as_view(), name="score_data"),
]
