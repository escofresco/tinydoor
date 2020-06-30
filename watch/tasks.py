from celery import shared_task

from config.celery_app import app
from doorknob import VideoDetect

@shared_task
def start_watching(file_url):
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
