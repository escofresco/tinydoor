import boto3
import json
import six

from moto import mock_sns_deprecated
from moto.core import ACCOUNT_ID

@mock_sns_deprecated
def test_create_and_delete_topic():
    conn = boto3.connect_sns()
    conn.create_topic("some-topic")

    topics_json = conn.get_all_topics()
    topics = topics_json["ListTopicsResponse"]["ListTopicsResult"]["Topics"]
    # topics.should.have.length_of(1)
    assert topics[0]["TopicArn"] == "arn:aws:sns:{0}:{1}:some-topic".format(conn.region.name, ACCOUNT_ID)
    # topics[0]["TopicArn"].should.equal(
    #     "arn:aws:sns:{0}:{1}:some-topic".format(conn.region.name, ACCOUNT_ID)
    # )

    # Delete the topic
    conn.delete_topic(topics[0]["TopicArn"])

    # And there should now be 0 topics
    topics_json = conn.get_all_topics()
    topics = topics_json["ListTopicsResponse"]["ListTopicsResult"]["Topics"]
    # topics.should.have.length_of(0)
    assert len(topics) == 0
