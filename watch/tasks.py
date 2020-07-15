from urllib.parse import urlparse

from celery import shared_task
from doorknob import Scene, VideoDetect
from watch.models import Score


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
    # add Score model with this score
    score = Score.objects.create(user=None,
                                 video_link=file_url,
                                 emotion_score=scene.valence)
    score.save()
    print(f'Score being saved? {score}')
    print(results)
    return {
        "score": scene.valence,
    }
