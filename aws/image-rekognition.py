import csv

# Boto3 is the AWS SDK for Python, which allows us to write software that makes use of services like Amazon S3
import boto3

with open("credentials.csv", "r") as input:
    next(input)
    reader = csv.reader(input)
    for line in reader:
        access_key_id = line[2]
        secret_accees_key = line[3]

key = "facial_expressions.jpeg"
bucket = "testing-objects"


def detect_faces(bucket, key, region="us-west-1", attributes=["ALL"]):
    client = boto3.client(
        "rekognition",
        region_name=region,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_accees_key,
    )
    #
    # # convert image to bytes
    # with open(key, 'rb') as source_image:
    #     source_bytes = source_image.read()

    # res = client.detect_faces(Image={'Bytes': source_bytes},
    #                           Attributes=attributes)

    res = client.detect_faces(
        Image={"S3Object": {"Bucket": bucket, "Name": key}}, Attributes=attributes
    )

    return res["FaceDetails"]


for face_detail in detect_faces(bucket, key):
    print(
        "Confidence level that the bounding box contains a face: {Confidence}".format(
            **face_detail
        )
    )
    print("Emotions: ")
    for emotion in face_detail["Emotions"]:
        print("   {Type}: {Confidence}%".format(**emotion))

    print("Gender: {Value} --> {Confidence}%".format(**face_detail["Gender"]))
    print("==============")
