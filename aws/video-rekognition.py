import csv
import boto3
import json
import sys


with open('credentials.csv', 'r') as input:
    next(input)
    reader = csv.reader(input)
    for line in reader:
        access_key_id = line[2]
        secret_accees_key = line[3]

bucket = 'aws-rekognition-un'
video = 'sample1.mp4'
rek = boto3.client('rekognition', region_name='us-west-1',
                      aws_access_key_id=access_key_id,
                      aws_secret_access_key = secret_accees_key)
# sqs = boto3.client('sqs')
# sns = boto3.client('sns')

# class VideoDetect:
#     def __init__(self, bucket, video):
#         self.jobId = ''
#         self.rek = boto3.client('rekognition', region_name='us-west-1',
#                             aws_access_key_id=access_key_id,
#                             aws_secret_access_key = secret_accees_key)
#         self.queueUrl = ''
#         self.roleArn = ''
#         self.topicArn = ''
#         self.bucket = bucket
#         self.video = video
#
#     # def main():
#     # """"""
#     #     job_found = False
#     #     sqs = boto3.client('sqs')
#     #
#     #     response = self.rek.start_face_detection(Video={
#     #                                                 'S3Object': {
#     #                                                     'Bucket': self.bucket,
#     #                                                     'Name': self.video,
#     #                                                 }
#     #                                             },
#     #                                             NotificationChannel={
#     #                                                 'SNSTopicArn': self.topicArn,
#     #                                                 'RoleArn': self.roleArn
#     #                                             },
#     #                                             FaceAttributes='ALL')
#     #
#
#     def get_people_results(self):
#         """"""
#         pass
#
#     def get_person_tracking(self):
#         """Get the path tracking
#        Start person tracking by calling start_person_tracking"""
#
#     def get_faces_results(self, job_id):
#         """Gets face dection results by calling get_face_detection
#            Start face detection by calling start_detection which returns a job_id"""
#         max_result = 10
#         pagination_token = ''
#         finished = False
#
#         # JobId: indentifier returned from start_face_detection
#         # NextToken: if the previous response was incomplete, Rek returns a pagination token.
#         while finished == False:
#             response = self.rek.get_face_detection(JobId=self.job_id,
#                                                    MaxResults=max_result,
#                                                    NextToken=pagination_token)
#
#         print(response['VideoMetadata']['Codec'])
#         print(str(response['VideoMetadata']['DurationMillis']))
#         print(response['VideoMetadata']['Format'])
#         print(response['VideoMetadata']['FrameRate'])
#
#         for face in response['Face']:
#             print('Face: ' + str(faceDetection['Face']))
#             print('Confidence: ' + str(faceDetection['Face']['Confidence']))
#             print('Timestamp: ' + str(faceDetection['Timestamp']))
#             print()
#
#         # If the response is truncated, Amazon Rekognition returns this token that you can use in the subsequent request to retrieve the next set of faces.
#         if 'NextToken' in response:
#             pagination_token = response['NextToken']
#         else: # If the response is complete.
#             finished = True
#
#     def start_detection(self):
#         """"""
#         response = self.rek.start_face_detection(
#             Video={
#                 'S3Object': {
#                     'Bucket': self.bucket,
#                     'Name': self.video,
#                 }
#             },
#             NotificationChannel={
#                 'SNSTopicArn': self.topicArn,
#                 'RoleArn': self.roleArn
#             },
#             FaceAttributes='ALL'
#         )
#
#         self.job_id = response['JobId']




###############################
jobId = ''
rek = boto3.client('rekognition', region_name='us-west-1',
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key = secret_accees_key)
queueUrl = ''
roleArn = ''
topicArn = ''


def get_faces_results(job_id):
    """Gets face dection results by calling get_face_detection
       Start face detection by calling start_detection which returns a job_id"""
    max_result = 10
    pagination_token = ''
    finished = False

    # JobId: indentifier returned from start_face_detection
    # NextToken: if the previous response was incomplete, Rek returns a pagination token.
    while finished == False:
        response = rek.get_face_detection(JobId=job_id,
                                           MaxResults=max_result,
                                           NextToken=pagination_token)

    print(response['VideoMetadata']['Codec'])
    print(str(response['VideoMetadata']['DurationMillis']))
    print(response['VideoMetadata']['Format'])
    print(response['VideoMetadata']['FrameRate'])

    for face in response['Face']:
        print('Face: ' + str(faceDetection['Face']))
        print('Confidence: ' + str(faceDetection['Face']['Confidence']))
        print('Timestamp: ' + str(faceDetection['Timestamp']))
        print()

    # If the response is truncated, Amazon Rekognition returns this token that you can use in the subsequent request to retrieve the next set of faces.
    if 'NextToken' in response:
        pagination_token = response['NextToken']
    else: # If the response is complete.
        finished = True

def start_detection(bucket, video):
    """"""
    response = rek.start_face_detection(
        Video={
            'S3Object': {
                'Bucket': bucket,
                'Name': video,
            }
        },
        # The Amazon SNS topic to which Amazon Rekognition to posts the completion status.
        # RoleArn: The ARN of an IAM role that gives Amazon Rekognition publishing permissions to the Amazon SNS topic.
        NotificationChannel={
            'SNSTopicArn': 'arn:aws:sns:us-west-1:468183285767:AWSRekognitionTopic',
            'RoleArn': 'arn:aws:iam::468183285767:role/rek-role'
        },
        FaceAttributes='ALL'
    )

    return response['JobId']


jobId = start_detection(bucket, video)
print(get_faces_results(jobId))
