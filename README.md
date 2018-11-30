## Perpetual program which runs on Raspberry Pi


1) ``` image_capture() ``` function captures an image at every 30 seconds and invokes ``` s3_upload() ``` thread 
2) ``` s3_upload() ``` uploads the image to AWS S3 bucket and invokes ``` face_recognition() ``` thread
3) ``` face_recognition() ``` gets response of all facial attributes(for all faces detetcted in image) from AWS rekognition and invokes ``` mongodb_upload() ``` thread
4) ``` mongodb_upload() ``` uploads the facial attributes data of all faces to a database which is hosted online
5) ``` face_matches() ``` indexes all the faces and compares them with exisiting data set. If there is any matching face, it will write to database