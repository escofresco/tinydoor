import os
# Boto3 is the AWS SDK for Python, which allows us to write software that makes use of services like Amazon S3
import boto3
from dotenv import load_dotenv
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')


key = 'happy_girl.jpg'
bucket = 'tinydoor-client-uploads'

def detect_faces(bucket, key, region='us-west-1', attributes=['ALL']):
    client = boto3.client('rekognition', region_name=region)
    #
    # # convert image to bytes
    # with open(key, 'rb') as source_image:
    #     source_bytes = source_image.read()

    # res = client.detect_faces(Image={'Bytes': source_bytes},
    #                           Attributes=attributes)

    res = client.detect_faces(Image={'S3Object': {
                                      'Bucket': bucket,
                                      'Name': key}
                                      },
                               Attributes=attributes)


    return res['FaceDetails']

for face_detail in detect_faces(bucket, key):
    print('Confidence level that the bounding box contains a face: {Confidence}'.format(**face_detail))
    print('Emotions: ')
    for emotion in face_detail['Emotions']:
        print("   {Type}: {Confidence}%".format(**emotion))

    print("Gender: {Value} --> {Confidence}%".format(**face_detail['Gender']))
    print('==============')
