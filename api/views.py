from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from watch.models import Score

from .serializers import ScoreSerializer


class ScoreData(APIView):
    """
    View to list the Scores for the videos that a user has created.
    """

    serializer_class = ScoreSerializer
    authentication_classes = list()
    permission_classes = list()

    def get(self, request, pk):
        """Return a list of emotion_scores and dates for all Scores
           associated with a given User.

           Parameters:
           request(HttpRequest): the GET request sent to the server
           pk (int): the id value of the User making the request

           Returns:
           Response: holds the data on the Scores from the database

        """
        # get the user
        User = get_user_model()
        user = User.objects.get(id=pk)
        # get the requested Score instances
        scores = Score.objects.filter(user=user)
        # structure the data
        score_data, score_dates = list(), list()
        for score in list(scores):
            # add the emotion score for this instancr
            score_data.append(score.emotion_score)
            # format the date and time shown for this score
            score_dates.append(
                f'{score.created.month}' + '/' +
                f'{score.created.day}' + '/' +
                f'{score.created.year} ' +
                f'{score.created.hour}' + ':' +
                f'{score.created.minute}' + ':' +
                f'{score.created.second}'
            )
        data = dict()
        data["scores"] = score_data
        data["dates"] = score_dates
        return Response(data)
