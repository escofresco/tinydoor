from __future__ import absolute_import, unicode_literals
import celery
from config.celery_app import app
from celery import shared_task
from .helpers import *
from .tasks import VideoDetect


@shared_task
def start_watching(file_url):
    vd = VideoDetect(file_url)
    return {
        "people_count": 33,
    }
