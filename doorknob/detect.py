import os
import boto3
import json
import sys
import time

from django.conf import settings


__all__ = ("VideoDetect", )

class VideoDetect:
    """Analyze videos using Rekognition Video API."""

    def __init__(self, video):
        self.video = video
        self.roleArn = settings.AWS_REKOGNITION_ROLE_ARN
        self.bucket = settings.AWS_CLIENT_UPLOADS_BUCKET_NAME
        kwargs = {
            "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
            "region_name": settings.AWS_REKOGNITION_REGION_NAME
        }
        session = boto3.Session(
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        self.rek = boto3.client("rekognition", **kwargs)
        self.sqs = boto3.client("sqs", **kwargs)
        self.sns = boto3.client("sns", **kwargs)
        self.startJobId = ""
        self.queueUrl = ""
        self.snsTopicArn = ""
        self.processType = ""


    def GetSQSMessageSuccess(self):

        jobFound = False
        succeeded = False

        dotLine = 0
        while jobFound == False:
            sqsResponse = self.sqs.receive_message(
                QueueUrl=self.sqsQueueUrl,
                MessageAttributeNames=["ALL"],
                MaxNumberOfMessages=10,
            )

            if sqsResponse:

                if "Messages" not in sqsResponse:
                    if dotLine < 40:
                        print(".", end="")
                        dotLine = dotLine + 1
                    else:
                        print()
                        dotLine = 0
                    sys.stdout.flush()
                    time.sleep(5)
                    continue

                for message in sqsResponse["Messages"]:
                    notification = json.loads(message["Body"])
                    rekMessage = json.loads(notification["Message"])
                    print(rekMessage["JobId"])
                    print(rekMessage["Status"])
                    if rekMessage["JobId"] == self.startJobId:
                        print("Matching Job Found:" + rekMessage["JobId"])
                        jobFound = True
                        if rekMessage["Status"] == "SUCCEEDED":
                            succeeded = True

                        self.sqs.delete_message(
                            QueueUrl=self.sqsQueueUrl,
                            ReceiptHandle=message["ReceiptHandle"],
                        )
                    else:
                        print(
                            "Job didn't match:"
                            + str(rekMessage["JobId"])
                            + " : "
                            + self.startJobId
                        )
                    # Delete the unknown message. Consider sending to dead letter queue
                    self.sqs.delete_message(
                        QueueUrl=self.sqsQueueUrl,
                        ReceiptHandle=message["ReceiptHandle"],
                    )

        return succeeded

    def StartLabelDetection(self):
        print(self.video)
        response = self.rek.start_label_detection(
            Video={"S3Object": {"Bucket": self.bucket, "Name": self.video}},
            NotificationChannel={
                "RoleArn": self.roleArn,
                "SNSTopicArn": self.snsTopicArn,
            },
        )

        self.startJobId = response["JobId"]
        print("Start Job Id: " + self.startJobId)

    def StartFaceDetection(self):
        response = self.rek.start_face_detection(
            Video={"S3Object": {"Bucket": self.bucket, "Name": self.video}},
            NotificationChannel={
                "RoleArn": self.roleArn,
                "SNSTopicArn": self.snsTopicArn,
            },
            FaceAttributes='ALL'
        )

        self.startJobId = response["JobId"]
        print("Start Job Id: " + self.startJobId)

    def GetLabelDetectionResults(self):
        maxResults = 10
        paginationToken = ""
        finished = False

        while finished == False:
            response = self.rek.get_label_detection(
                JobId=self.startJobId,
                MaxResults=maxResults,
                NextToken=paginationToken,
                SortBy="TIMESTAMP",
            )

            print("Codec: " + response["VideoMetadata"]["Codec"])
            print("Duration: " + str(response["VideoMetadata"]["DurationMillis"]))
            print("Format: " + response["VideoMetadata"]["Format"])
            print("Frame rate: " + str(response["VideoMetadata"]["FrameRate"]))
            print()

            for labelDetection in response["Labels"]:
                label = labelDetection["Label"]

                print("Timestamp: " + str(labelDetection["Timestamp"]))
                print("   Label: " + label["Name"])
                print("   Confidence: " + str(label["Confidence"]))
                print("   Instances:")
                for instance in label["Instances"]:
                    print("      Confidence: " + str(instance["Confidence"]))
                    print("      Bounding box")
                    print("        Top: " + str(instance["BoundingBox"]["Top"]))
                    print("        Left: " + str(instance["BoundingBox"]["Left"]))
                    print("        Width: " + str(instance["BoundingBox"]["Width"]))
                    print("        Height: " + str(instance["BoundingBox"]["Height"]))
                    print()
                print()
                print("   Parents:")
                for parent in label["Parents"]:
                    print("      " + parent["Name"])
                print()

                if "NextToken" in response:
                    paginationToken = response["NextToken"]
                else:
                    finished = True

    def GetFaceDetectionResults(self):
        """
        Return an array of detected faces (Faces) sorted by the time the faces were detected.
        Get the results of face detection by calling get_face_detection().

        Expected output:
            Emotions: [
                {'Type': string, 'Confidence': number},
            ]
        """
        maxResults = 10
        paginationToken = ""
        finished = False
        results = []

        while finished == False:
            response = self.rek.get_face_detection(
                JobId=self.startJobId,
                MaxResults=maxResults,
                NextToken=paginationToken
            )
            results.append(response)

            if "NextToken" in response:
                paginationToken = response["NextToken"]
            else:
                finished = True
        return results

    def CreateTopicandQueue(self):

        millis = str(int(round(time.time() * 1000)))

        # Create SNS topic

        snsTopicName = "AmazonRekognitionTinyDoor" + millis

        topicResponse = self.sns.create_topic(Name=snsTopicName)
        self.snsTopicArn = topicResponse["TopicArn"]
        print(self.snsTopicArn)

        # create SQS queue
        sqsQueueName = "AmazonRekognitionQueue" + millis
        self.sqs.create_queue(QueueName=sqsQueueName)
        self.sqsQueueUrl = self.sqs.get_queue_url(QueueName=sqsQueueName)["QueueUrl"]

        attribs = self.sqs.get_queue_attributes(
            QueueUrl=self.sqsQueueUrl, AttributeNames=["QueueArn"]
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
            QueueUrl=self.sqsQueueUrl, Attributes={"Policy": policy}
        )

    def DeleteTopicandQueue(self):
        self.sqs.delete_queue(QueueUrl=self.sqsQueueUrl)
        self.sns.delete_topic(TopicArn=self.snsTopicArn)
