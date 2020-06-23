from __future__ import absolute_import, unicode_literals
import celery
from config.celery_app import app
from celery import shared_task
from .helpers import *


@shared_task
def start_watching(file_url):
    return {
        'people_count': 33,
    }
