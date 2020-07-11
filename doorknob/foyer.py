"""
Manage the events detected through computer vision of a central space.
"""
from collections import Counter
from decimal import Decimal
from math import sqrt

__all__ = ("Scene",)


class Scene:
    """
    Aggregate time-series data from objects in a cohesive narrative.

    Attributes:
        aws_data: A list of detected face json objects generated by AWS
                   Rekognition.
        valence(float): the emotion detection score of the video uploaded
    """

    def __init__(self, aws_data=None):
        self.aws_data = aws_data
        self.__valence = self.score(*zip(*self.faces_as_valence_scores(self.aws_data)))

    def faces_as_valence_scores(self, aws_data):
        """
        Pass through AWS detected faces and calculate valence score for each.

        Args:
            aws_faces: Data generated by AWS face detection.

        Yields:
            Valence of next face
        """
        for timestep in aws_data:
            faces = timestep.get("Faces")

            if faces is None:
                raise ValueError("aws data is missing Faces")

            for face in faces:
                face = face.get("Face")

                if face is None:
                    raise ValueError("aws data is missing Face")

                if "Emotions" in face:
                    yield self.emotions_valence(face["Emotions"])
                else:
                    raise ValueError("aws data is missing emotions")

    def emotions_valence(self, emotions):
        """
        Reduce list of emotions of a single number representing the valence.

        Args:
            emotions: [
                    {
                        'Type': 'HAPPY'|'SAD'|'ANGRY'|'CONFUSED'|'DISGUSTED'|
                        'SURPRISED'|'CALM'|'UNKNOWN'|'FEAR',
                        'Confidence': ...
                    },
                ]
        Returns:
            (1, confidence) if positive, (0, confidence) if neutral,
            (-1, confidence) if negative.
        """
        positive = {"HAPPY", "CALM"}
        negative = {"ANGRY", "CONFUSED", "DISGUSTED", "FEAR"}
        most_likely_emotion = (0, "UNKNOWN")

        for emotion in emotions:
            emotion_type = emotion["Type"]
            emotion_confidence = emotion["Confidence"]

            if emotion_confidence > most_likely_emotion[0]:
                most_likely_emotion = (emotion_confidence, emotion_type)
        if most_likely_emotion[1] in positive:
            return (1, most_likely_emotion[0])
        elif most_likely_emotion[1] in negative:
            return (-1, most_likely_emotion[0])
        return (0, most_likely_emotion[0])

    @property
    def valence(self):
        return self.__valence
        # return self.score(*zip(*self.faces_as_valence_scores(self.aws_data)))

    def score(self, ratings, weights, scale=100, M=100, P=0.5):
        """
        A weighted scoring algorithm. Adapted from https://tinyurl.com/y88kvfth.

        Args:
            ratings: Array of valence ratings which can either be -1, 0, or 1.
            weights: Array of corresponding weights for each score ∈ [0, 1].
            M: A number representing a moderate value.
            P:  ∈ [0, 1]

        Returns:
            A score ∈ [0, 1]
        """
        assert len(ratings) == len(weights)
        hist = Counter(ratings)

        # Number of elements
        n = Decimal(len(ratings))

        # https://tinyurl.com/y2ka4gja
        # (1-confidence/2) quantile of the standard normal distribution
        # where confidence == .95
        z = Decimal(1.96)

        # Observed fraction of positive ratings
        p_hat = Decimal(hist[1]) / n

        # Lower bound of Wilson score confidence interval for a Bernoulli parameter
        return (
            p_hat
            + z * z / (2 * n)
            - z * Decimal(sqrt((p_hat * (1 - p_hat) + z * z / (4 * n)) / n))
        ) / (1 + z * z / n)
        #
        # # Quantity importance
        # Q = -Decimal(M) / Decimal(1 / 2).ln()
        #
        # # Weighted mean
        # p = sum(Decimal(r + 1) * Decimal(w) for r, w in zip(ratings, weights)) / n
        # # Normalized mean
        # # p = sum(Decimal(num)*Decimal(count) for num, count in hist.items()) / q
        #
        # return Decimal(P) * Decimal(p) + Decimal(2) * (1 - Decimal(P)) * (
        #     1 - Decimal(-n / Q).exp()
        # )
