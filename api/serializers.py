from rest_framework.serializers import ModelSerializer
from watch.models import Score


class ScoreSerializer(ModelSerializer):
    class Meta:
        model = Score
        fields = "__all__"
