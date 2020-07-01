import json
import os
import unittest

from doorknob.foyer import Scene

class SceneTestCase(unittest.TestCase):
    def test_valence(self):
        filename = "doorknob/tests/long_rekognition_face_response.txt"
        with open(filename) as f:
            scene = Scene(aws_data=json.load(f))
        print(list(scene.valence))
