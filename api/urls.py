from api.views import ScoreData
from django.urls import path

urlpatterns = [
    path("<int:pk>/", ScoreData.as_view(), name="score_data"),
]
