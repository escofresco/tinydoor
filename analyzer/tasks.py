from __future__ import absolute_import, unicode_literals

from config.celery_app import app
from celery import shared_task
from .helpers import *


@shared_task
def start_watching(file_url):
    """Transcribes a file by its location in S3 and then applies AWS Comprehend
    actions to the transcript.
    Args:
        filename: The full url to an audio file in S3.
    Returns:
        {
            'text_content': str,
            'language': str,
            'sentiment': str,
        }
    """
    transcribe_res = transcribe(file_url)
    job = transcribe_res["TranscriptionJob"]

    if job["TranscriptionJobStatus"] == "FAILED":
        raise Exception("Transcript failed to complete")
    transcribe_uri = job["Transcript"]["TranscriptFileUri"]
    transcript_res = load_json_from_uri(transcribe_uri)
    content = transcript_res["results"]["transcripts"][0]["transcript"]

    comprehend_res = comprehend(content)
    return {"text_content": content, **comprehend_res}
