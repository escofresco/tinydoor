import os
import boto3
import json
import sys
import time

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
region_name = "us-west-1"


class VideoDetect:
    """Analyze videos using Rekognition Video API."""

    rek = boto3.client("rekognition", region_name)
    sqs = boto3.client("sqs", region_name)
    sns = boto3.client("sns", region_name)
    startJobId = ""
    queueUrl = ""
    snsTopicArn = ""
    processType = ""

    def __init__(self, role, bucket, video):
        self.roleArn = role
        self.bucket = bucket
        self.video = video

    def GetResultsFaces(self, jobId):
        """
        Return an array of detected faces (Faces) sorted by the time the faces were detected.
        Get the results of face detection by calling get_face_detection().

        Expected output:
            Emotions: [
                {'Type': string, 'Confidence': number},
            ]
        """
        maxResults = 30
        paginationToken = ""
        finished = False

        while finished == False:
            response = self.rek.get_face_detection(
                JobId=jobId, MaxResults=maxResults, NextToken=paginationToken
            )

            for faceDetection in response["Faces"]:
                max = faceDetection["Face"]["Emotions"][0]
                for emotion in faceDetection["Face"]["Emotions"]:
                    if emotion["Confidence"] > max["Confidence"]:
                        max = emotion
                print(max)
                print()

            if "NextToken" in response:
                paginationToken = response["NextToken"]
            else:
                finished = True

    def GetResultsPersons(self, jobId):
        """Get person tracking information by calling get_person_tracking()."""
        maxResults = 30
        paginationToken = ""
        finished = False

        while finished is False:
            response = self.rek.get_person_tracking(
                JobId=jobId, MaxResults=maxResults, NextToken=paginationToken
            )

            print(response["VideoMetadata"]["Codec"])
            print(str(response["VideoMetadata"]["DurationMillis"]))
            print(response["VideoMetadata"]["Format"])
            print(response["VideoMetadata"]["FrameRate"])

            for personDetection in response["Persons"]:
                print("Index: " + str(personDetection["Person"]["Index"]))
                print("Timestamp: " + str(personDetection["Timestamp"]))
                print()

            if "NextToken" in response:
                paginationToken = response["NextToken"]
            else:
                finished = True

    def CreateTopicandQueue(self):
        """Create a topic to which notifications can be published."""
        millis = str(int(round(time.time() * 1000)))

        # Create SNS topic
        snsTopicName = "AmazonRekognition-TinyDoor" + millis

        topicResponse = self.sns.create_topic(Name=snsTopicName)
        self.snsTopicArn = topicResponse["TopicArn"]

        # create SQS queue
        sqsQueueName = "AmazonRekognitionQueue" + millis
        self.sqs.create_queue(QueueName=sqsQueueName)
        self.queueUrl = self.sqs.get_queue_url(QueueName=sqsQueueName)["QueueUrl"]

        attribs = self.sqs.get_queue_attributes(
            QueueUrl=self.queueUrl, AttributeNames=["QueueArn"]
        )["Attributes"]

        sqsQueueArn = attribs["QueueArn"]

        # Subscribe SQS queue to SNS topic
        self.sns.subscribe(
            TopicArn=self.snsTopicArn, Protocol="sqs", Endpoint=sqsQueueArn
        )

        # Authorize SNS to write SQS queue
        policy = """{{
          "Version":"2012-10-17",
          "Statement":[
            {{
              "Sid":"MyPolicy",
              "Effect":"Allow",
              "Principal" : {{"AWS" : "*"}},
              "Action":"SQS:SendMessage",
              "Resource": "{}",
              "Condition":{{
                "ArnEquals":{{
                  "aws:SourceArn": "{}"
                }}
              }}
            }}
          ]
        }}""".format(
            sqsQueueArn, self.snsTopicArn
        )

        response = self.sqs.set_queue_attributes(
            QueueUrl=self.queueUrl, Attributes={"Policy": policy}
        )

    def DeleteTopicandQueue(self):
        """Deletes a topic and all its subscriptions."""
        self.sqs.delete_queue(QueueUrl=self.queueUrl)
        self.sns.delete_topic(TopicArn=self.snsTopicArn)

    def main(self):
        """
        Start analysis of video in specified bucket.
        Face detection is started by a call to start_face_detection.
        """
        jobFound = False
        response = self.rek.start_face_detection(
            Video={"S3Object": {"Bucket": self.bucket, "Name": self.video}},
            NotificationChannel={
                "RoleArn": self.roleArn,
                "SNSTopicArn": self.snsTopicArn,
            },
            FaceAttributes="ALL",
        )

        # response = self.rek.start_person_tracking(Video={'S3Object':{'Bucket':self.bucket,'Name':self.video}},
        # NotificationChannel={'RoleArn':self.roleArn, 'SNSTopicArn':self.snsTopicArn})

        print("Start Job Id: " + response["JobId"])
        dotLine = 0
        while jobFound is False:
            sqsResponse = self.sqs.receive_message(
                QueueUrl=self.queueUrl,
                MessageAttributeNames=["ALL"],
                MaxNumberOfMessages=10,
            )

            if sqsResponse:
                if "Messages" not in sqsResponse:
                    if dotLine < 20:
                        print(".", end="")
                        dotLine = dotLine + 1
                    else:
                        print()
                        dotLine = 0
                    sys.stdout.flush()
                    continue

                for message in sqsResponse["Messages"]:
                    notification = json.loads(message["Body"])
                    rekMessage = json.loads(notification["Message"])
                    print(rekMessage["JobId"])
                    print(rekMessage["Status"])
                    if str(rekMessage["JobId"]) == response["JobId"]:
                        print("Matching Job Found:" + rekMessage["JobId"])
                        jobFound = True
                        self.GetResultsFaces(rekMessage["JobId"])
                        self.sqs.delete_message(
                            QueueUrl=self.queueUrl,
                            ReceiptHandle=message["ReceiptHandle"],
                        )
                    else:
                        print(
                            "Job didn't match:"
                            + str(rekMessage["JobId"])
                            + " : "
                            + str(response["JobId"])
                        )
                    # Delete the unknown message. Consider sending to dead letter queue
                    self.sqs.delete_message(
                        QueueUrl=self.queueUrl, ReceiptHandle=message["ReceiptHandle"]
                    )

        print("done")


if __name__ == "__main__":
    roleArn = "arn:aws:iam::623782584215:role/tinydoor-rekognition"
    bucket = "tinydoor-client-uploads"
    video = "emotion-test/Screen Recording 2020-06-28 at 12.52.49 PM.mov"

    analyzer = VideoDetect(roleArn, bucket, video)
    analyzer.CreateTopicandQueue()
    analyzer.main()
    analyzer.DeleteTopicandQueue()
