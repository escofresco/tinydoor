from rest_framework.response import Response
from rest_framework.views import APIView
from watch.models import Score

from .serializers import ScoreSerializer


class ScoreData(APIView):
    """
    View to list the Scores for the videos that a user has received.
    """

    serializer_class = ScoreSerializer
    authentication_classes = list()
    permission_classes = list()

    def get(self, request):
        """Return a list of emotion_scores and dates for all Scores
           associated with a given User.

           Parameters:
           request(HttpRequest): the GET request sent to the server

           Returns:
           Response: holds the data on the Scores from the database

        """
        # get the requested Score instances
        scores = Score.objects.get(user=request.user)
        # structure the data
        data = [score.emotion_score for score in scores]
        return Response(data)
