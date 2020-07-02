import boto3

from django.conf import settings

def delete_all_topics():
    """
    Delete all SNS topics using aws config from settings.
    """
    sns = boto3.client("sns", aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                       aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                       region_name=settings.AWS_REKOGNITION_REGION_NAME)

    for elm in sns.list_topics()["Topics"]:
        sns.delete_topic(TopicArn=elm["TopicArn"])

def delete_all_queues():
    """
    Delete all SQS queues using aws config from settings.
    """
    sqs = boto3.client("sqs", aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                       aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                       region_name=settings.AWS_REKOGNITION_REGION_NAME)

    for url in sqs.list_queues()["QueueUrls"]:
        sqs.delete_queue(QueueUrl=url)
