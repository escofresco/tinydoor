import json
import unittest

from doorknob.foyer import Scene
<<<<<<< HEAD
=======

>>>>>>> 7947f58b3010bd6e94e4351e2d33a23f81608875

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


class VideoDetectTestCase(unittest.TestCase):
    """
    Tests that the VideoDetect properties and functions work correctly.
    """
