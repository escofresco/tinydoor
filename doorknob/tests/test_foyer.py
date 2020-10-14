import json
import unittest

from doorknob.foyer import Scene

class SceneTestCase(unittest.TestCase):
    def test_valence(self):
        filename = "doorknob/tests/long_rekognition_face_response.txt"
        with open(filename) as f:
            scene = Scene(aws_data=json.load(f))
        assert scene.valence > 0.5

    def test_no_emotions(self):
        filename = "doorknob/tests/no_emotions_rekognition_face_response.txt"
        with open(filename) as f:
            with self.assertRaises(ValueError):
                Scene(aws_data=json.load(f))
