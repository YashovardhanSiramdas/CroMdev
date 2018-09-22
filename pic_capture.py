# This program will run perpetually on Raspberry Pi
import os
import datetime
import time
import boto3
from threading import Thread
import json

def face_recognition(image_name):
    response = rekognition.detect_faces(
        Image={
            "S3Object": {
                "Bucket": BUCKET,
                "Name": image_name
            }
        },
        Attributes=["ALL"],
    )
    print json.dumps(response["FaceDetails"], indent=4)


def s3_upload(image_name):
    data = open(image_name,"rb")
    s3.Bucket(BUCKET).put_object(Key=image_name, Body=data)
    image_analysis = Thread(target=face_recognition,args=[image_name])
    image_analysis.start()


def image_capture():
    image_name = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H:%M:%S")
    os.system("fswebcam -d /dev/video0 -r 720x480 "+image_name+".jpeg")
    image_upload = Thread(target=s3_upload,args=[image_name+".jpeg"])
    image_upload.start()

s3 = boto3.resource("s3")
rekognition = boto3.client("rekognition", "us-east-2")
BUCKET = "cromdev"
t=20     
i=1       

while True:
    x=Thread(target=image_capture)
    x.start()
    print (i)       

    i=i+1
    time.sleep(t)   
