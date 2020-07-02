from urllib.parse import urlparse

from celery import shared_task
from doorknob import Scene, VideoDetect


@shared_task
def start_watching(file_url):
    file_path = urlparse(file_url).path.strip("/")
    analyzer = VideoDetect(file_path)
    results = None
    analyzer.CreateTopicandQueue()
    analyzer.StartFaceDetection()

    if analyzer.GetSQSMessageSuccess():
        results = analyzer.GetFaceDetectionResults()
    analyzer.DeleteTopicandQueue()
    scene = Scene(results)
    print(results)
    return {
        "score": scene.valence,
    }
