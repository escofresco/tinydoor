from rest_framework.response import Response
from rest_framework.views import APIView
from watch.models import Score

from .serializers import ScoreSerializer


class ScoreData(APIView):
    """View to list the times a user has achieved or failed at a Goal."""

    serializer_class = ScoreSerializer
    authentication_classes = list()
    permission_classes = list()

    def get(self, request, pk, format=None):
        """Return a list of the data for one Goal with fields and values.
           request(HttpRequest): the GET request sent to the server
           pk(int): unique id value of an Goal instance
           format(str): the suffix applied to the endpoint to indicate how the
                        data is structured (i.e. html, json)
           Returns:
           Response: holds the data on the Goal from the database
        """
        # get the requested Goal instance
        goal = Score.objects.get(id=pk)
        data = {
            "labels": ["Achievements", "Fails"],
            "values": [goal.achievements, goal.fails],
        }
        return Response(data)
