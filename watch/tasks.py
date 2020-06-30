from celery import shared_task

from config.celery_app import app
from doorknob import VideoDetect

@shared_task
def start_watching(file_url):
    file_url = "02/f7f67761e143178c17e4967329a5d1/Untitled.mp4"
    analyzer = VideoDetect(file_url)
    results = None
    analyzer.StartLabelDetection()

    if analyzer.GetSQSMessageSuccess() == True:
        results = analyzer.GetLabelDetectionResults()
    analyzer.DeleteTopicandQueue()
    return results
    # return {
    #
    #     "people_count": 33,
    # }
