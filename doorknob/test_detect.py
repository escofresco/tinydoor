import re
import unittest

import boto3
from freezegun import freeze_time
from moto import mock_sns, mock_sqs

# from moto.core import ACCOUNT_ID

ACCOUNT_ID = "123456789012"

MESSAGE_FROM_SQS = (
    '{\n  "Message": "%s",\n  "MessageId": "%s",\n '
    + '"Signature":"EXAMPLElDMXvB8r9R83tGoNn0ecwd5UjllzsvSvbItzfaMpN2nk5HVSw7'
    + "XnOn/49IkxDKz8YrlH2qJXj2iZB0Zo2O71c4qQk1fMUDi3LGpij7RCW7AW9vYYsSqIKRnFS"
    + '94ilu7NFhUzLiieYr4BKHpdTmdD6c0esKEYBpabxDSc=",\n  "SignatureVersion": '
    + '"1",\n  "SigningCertURL": "https://sns.us-west-1.amazonaws.com/'
    + 'SimpleNotificationService-f3ecfb7224c7233fe7bb5f59f96de52f.pem",\n  '
    + '"Subject": "my subject",\n  "Timestamp": "2020-07-24T12:00:00.000Z",\n'
    + '  "TopicArn": "arn:aws:sns:%s:'
    + ACCOUNT_ID
    + ':some-topic",\n'
    + '"Type": "Notification",\n'
    + '"UnsubscribeURL":'
    + '"https://sns.us-west-1.amazonaws.com/?Action='
    + "Unsubscribe&SubscriptionArn=arn:aws:sns:us-west-1:"
    + ACCOUNT_ID
    + ':some-topic:2bcfbf39-05c3-41de-beaa-fcfcc21c8f55"\n}'
)


class VideoDetectTestCase(unittest.TestCase):
    """
    Tests that the VideoDetect properties and functions work correctly.
    """

    @mock_sqs
    @mock_sns
    def test_publish_result_to_sqs(self):
        conn = boto3.client("sns", region_name="us-west-1")
        conn.create_topic(Name="some-topic")
        response = conn.list_topics()
        topic_arn = response["Topics"][0]["TopicArn"]

        sqs_conn = boto3.resource("sqs", region_name="us-west-1")
        sqs_conn.create_queue(QueueName="test-queue")

        conn.subscribe(
            TopicArn=topic_arn,
            Protocol="sqs",
            Endpoint="arn:aws:sqs:us-west-1:{}:test-queue".format(ACCOUNT_ID),
        )
        message = "my message"

        with freeze_time("2020-07-24 12:00:00"):
            published_message = conn.publish(TopicArn=topic_arn, Message=message)
        published_message_id = published_message["MessageId"]

        # fetch queue
        queue = sqs_conn.get_queue_by_name(QueueName="test-queue")
        messages = queue.receive_messages(MaxNumberOfMessages=1)

        expected = MESSAGE_FROM_SQS % (message, published_message_id, "us-west-1")
        acquired_message = re.sub(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z",
            "2020-07-24T12:00:00.000Z",
            messages[0].body,
        )
        # print("Acquired: ", acquired_message)
        # print("Expected: ", expected)
        # print(messages[0].body)

        assert acquired_message == expected

    @mock_sns
    def test_create_and_delete_topic(self):
        conn = boto3.client("sns", region_name="us-west-1")
        topic_name = "some-topic"
        conn.create_topic(Name=topic_name)

        topics_json = conn.list_topics()
        topics = topics_json["Topics"]
        assert len(topics) == 1
        assert topics[0]["TopicArn"] == "arn:aws:sns:{0}:{1}:{2}".format(
            conn._client_config.region_name, ACCOUNT_ID, topic_name
        )

        # Delete the topic
        conn.delete_topic(TopicArn=topics[0]["TopicArn"])

        # And there should now be 0 topics
        topics_json = conn.list_topics()
        topics = topics_json["Topics"]
        assert len(topics) == 0

    @mock_sqs
    def test_create_and_delete_queue(self):
        sqs = boto3.client("sqs", region_name="us-west-1")
        sqs.create_queue(QueueName="test-queue")

        queues_json = sqs.list_queues()
        assert len(queues_json["QueueUrls"]) == 1

        queue_url = sqs.get_queue_url(QueueName="test-queue")["QueueUrl"]
        assert queue_url.split("/")[-1] == "test-queue"
        assert queue_url.split("/")[2].split(".")[0] == "us-west-1"

        # Delete the topic
        sqs.delete_queue(QueueUrl=queue_url)
        queues_json = sqs.list_queues()
        assert "QueueUrls" not in queues_json


if __name__ == "__main__":
    unittest.main()
