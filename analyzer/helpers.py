import os
import requests
import time
import uuid
import json

import boto3
from botocore.exceptions import ClientError, NoCredentialsError


def load_json_from_uri(uri):
    return requests.get(uri).json()


def transcribe(job_uri):
    '''Wrapper for AWS Transcribe API'''
    transcribe = boto3.client(
        'transcribe',
        aws_access_key_id=os.getenv('DJANGO_AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('DJANGO_AWS_SECRET_ACCESS_KEY'),
        region_name='us-west-1',
    )
    job_name = str(uuid.uuid4())
    # job_uri = f'https:///really-listening-client-uploads.s3-us-west-1.amazonaws.com/{filename}'
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        LanguageCode='en-US',
    )
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in [
            'COMPLETED',
            'FAILED',
        ]:
            break
        time.sleep(5)
    return status


def comprehend(text):
    '''Wrapper for AWS Comprehend API.
    Returns:
        {
            'language': str,
            'sentiment': str,
        }
    '''
    comprehend = boto3.client(
        'comprehend',
        aws_access_key_id=os.getenv('DJANGO_AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('DJANGO_AWS_SECRET_ACCESS_KEY'),
        region_name='us-west-2',
    )
    job_name = str(uuid.uuid4())

    print('Calling DetectDominantLanguage')
    dominant_lang_res = comprehend.detect_dominant_language(Text = text)
    print(dominant_lang_res)
    print(json.dumps(dominant_lang_res, sort_keys=True, indent=4))
    print('End of DetectDominantLanguage\n')

    print('Calling DetectSentiment')
    sentiment_res = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    print(json.dumps(sentiment_res, sort_keys=True, indent=4))
    print('End of DetectSentiment\n')

    print('Calling DetectKeyPhrases')
    key_phrases = comprehend.detect_key_phrases(Text=text, LanguageCode='en')
    print(json.dumps(key_phrases, sort_keys=True, indent=4))
    print('End of DetectKeyPhrases\n')

    dominant_lang = dominant_lang_res['Languages'][0]['LanguageCode']
    dominant_sentiment = sentiment_res['Sentiment']
    return {
        'language': dominant_lang,
        'sentiment': dominant_sentiment
    }