# This Program runs prepetually on Raspberry Pi
#
# Work Flow:-
# 1) image_capture() function captures an image at every 30 seconds and invokes s3_upload() thread 
# 2) s3_upload() uploads the image to AWS S3 bucket and invokes face_recognition() thread
# 3) face_recognition() gets response of all facial attributes(for all faces detetcted in image) from AWS rekognition and invokes mongodb_upload() thread
# 4) mongodb_upload() uploads the facial attributes data of all faces to a database which is hosted online
import os
import datetime
import time
import boto3
from threading import Thread
import json
from pymongo import MongoClient

def mongodb_upload(response,image_name):
    try:
        collection1.insert_one({
            "image_name": image_name,
            "face_count": len(response)
            })
        print("successfully inserted face count")

        for record in response:
            collection2.insert_one({
                "image_name": image_name,
                "confidence": record["Confidence"],
                "eyeglasses_confidence": record["Eyeglasses"]["Confidence"],
                "eyeglasses_value": record["Eyeglasses"]["Value"],
                "sunglasses_confidence": record["Sunglasses"]["Confidence"],
                "sunglasses_value": record["Sunglasses"]["Value"], 
                "gender_confidence": record["Gender"]["Confidence"],
                "gender_value": record["Gender"]["Value"],
                "emotion1_confidence": record["Emotions"][0]["Confidence"],
                "emotion1_value": record["Emotions"][1]["Type"],
                "emotion2_confidence": record["Emotions"][0]["Confidence"],
                "emotion2_value": record["Emotions"][1]["Type"],
                "emotion3_confidence": record["Emotions"][2]["Confidence"],
                "emotion3_value": record["Emotions"][2]["Type"],
                "age_range_high": record["AgeRange"]["High"],
                "age_range_low": record["AgeRange"]["Low"],
                "eyesopen_confidence": record["EyesOpen"]["Confidence"],
                "eyesopen_value": record["EyesOpen"]["Value"],
                "smile_confidence": record["Smile"]["Confidence"],
                "smile_value": record["Smile"]["Value"],
                "mouthopen_confidence": record["MouthOpen"]["Confidence"],
                "mouthopen_value": record["MouthOpen"]["Value"],
                "mustache_confidence": record["Mustache"]["Confidence"],
                "mustache_value": record["Mustache"]["Value"],
                "beard_confidence": record["Beard"]["Confidence"],
                "beard_value": record["Beard"]["Value"]
                })
            print("successfully inserted face metrics") 
        
    except Exception,e:
        print str(e)

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
    store_data = Thread(target=mongodb_upload,args=[response["FaceDetails"],image_name])
    store_data.start()


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

client = MongoClient('mongodb://cromdev:cromdev1234@ds249249.mlab.com:49249/cromdev')
db = client.cromdev
collection1 = db.face_count
collection2 = db.face_metrics

s3 = boto3.resource("s3")
rekognition = boto3.client("rekognition", "us-east-2")
BUCKET = "cromdev"
t=30
i=1       

while True:
    init=Thread(target=image_capture)
    init.start()
    print (i)
    i=i+1
    time.sleep(t)   
