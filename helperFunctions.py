
import requests
import json
import cv2
import certifi
from pymongo import MongoClient
import base64
import numpy as np

def loginUser():
    loginUrl = "http://jackettbackend-v1-prod.ap-southeast-1.elasticbeanstalk.com/api/v1/auth/login"
    login_headers = {"accept": "application/json",
                    "content-type": "application/json"
                    }
    login_data = {"username":"jeemain12mathsarihantDS",
            "password":"jeemain12mathsarihantDS"}
        
    respLogin = requests.post(url=loginUrl, headers=(login_headers), data=json.dumps(login_data))
    respLoginJson = respLogin.json()
    token = respLoginJson['data']['token']

    return token

TOKEN = loginUser()

headers = {"accept": "application/json",
                 "content-type": "application/json"
                }
headers['authorization'] = "Bearer " + str(TOKEN)

MONGO_URLdev = "mongodb+srv://mongo_jackett:fCmWGwxTJYiq3znL@cluster0.elr48.mongodb.net/test?retryWrites=true&w=majority"
clientDev = MongoClient(MONGO_URLdev, tlsCAFile=certifi.where())
dbToUseDev = clientDev.test
bbColDev = dbToUseDev.bounding_box

def retrieveAnnotation(sourceImageId):
    annotationDataTemp = list(bbColDev.find({'imageKey':sourceImageId}, {'updatedCoordinates':1}))
    return annotationDataTemp[0]['updatedCoordinates']

def retrieveImageFromS3(sourceImageId):
    DOWNLOAD_IMAGE_URL = "http://jackettbackend-v1-prod.ap-southeast-1.elasticbeanstalk.com/api/resource/" + sourceImageId + "/download-image"
    r = requests.get(DOWNLOAD_IMAGE_URL, headers=headers)
    imageData = r.json()['data']['fileData']
    
    decoded_data = base64.b64decode(imageData)
    np_data = np.fromstring(decoded_data,np.uint8)
    omrImageRaw = cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)

    annotationsTemp = retrieveAnnotation(sourceImageId)
    print(annotationsTemp[0])
    for i in annotationsTemp:
        xmin = int(i['xmin'])
        xmax = int(i['xmax'])
        ymin = int(i['ymin'])
        ymax = int(i['ymax'])

        width = xmax-xmin
        height= ymax-ymin
        print(xmin,ymin,width,height)
        img = cv2.rectangle(omrImageRaw, (xmin,ymin),(xmax,ymax),(0,0,255), 2)

    return omrImageRaw