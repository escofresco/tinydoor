from urllib.parse import urlparse

from celery import shared_task

from config.celery_app import app
from doorknob import VideoDetect

@shared_task
def start_watching(file_url):
    file_path = urlparse(file_url).path
    analyzer = VideoDetect(file_path)
    results = None
    analyzer.CreateTopicandQueue()
    analyzer.StartFaceDetection()

    if analyzer.GetSQSMessageSuccess() == True:
        results = analyzer.GetFaceDetectionResults()#.GetLabelDetectionResults()
    analyzer.DeleteTopicandQueue()
    print(results)
    return {

        "people_count": results,
    }
