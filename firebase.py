import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
import os
from detect import lpr
from datetime import datetime


cred = credentials.Certificate("serviceAccountKey/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

pid = 'ChIJDfytRslyhlQRjB7JJRA9fSo'
db = firestore.client()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.IN)

camera = PiCamera()

while True:
    print('started')
    # get the value for val
    val = GPIO.input(3)

    # if val = 1 stay in loop
    while(val == 1):
        val = GPIO.input(3)

    # check car on spot for more than a minute
    t = datetime.now()
    delta = datetime.now() - t
    while(val == 0 and delta.seconds < 60):
        val = GPIO.input(3)
        delta = datetime.now() - t
        # define flag

    # if(delta.seconds < 60):
    #     continue

    print('picture in 10 seconds')
    sleep(10)
    # now take a picture of the car
    now = datetime.now()
    dt = now.strftime("%d%m%Y%H:%M:%S")
    name = dt + ".jpg"
    camera.capture(name)
    print('picture taken')

    sleep(1)
    print('starting lpr')
    # send file to detect.py and get string
    path = os.path.abspath(name)
    path = '/home/pi/Desktop/RPiBackend/data/images/car2.jpg'
    print(path)
    print(type(path))
    lpn = lpr(path)
    #lpn = 'STA5131E'

    print(lpn)
    print('finding user')

    userdoc = db.collection("ParkingUsers").where("lpn", "==", lpn).get()
    for doc in userdoc:
        key = doc.id
        req = db.collection("ParkingRequest").document(pid).collection('requests').document(key).get()
        if req.to_dict() is not None:
            progress = req.to_dict()['progress']
            uid = req.to_dict()['uid']
            if(uid == doc.id and progress == 'AwaitingConfirmation'):
                print("updating to confirmed")
                db.collection("ParkingRequest").document(pid).collection('requests').document(key).update({"progress":"Confirmed"})
                break

    userdoc = db.collection("ParkingUsers").get()
    for doc in userdoc:
        key = doc.id
        req = db.collection("ParkingRequest").document(pid).collection('requests').document(key).get()
        if req.to_dict() is not None:
            progress = req.to_dict()['progress']
            uid = req.to_dict()['uid']
            if(uid == doc.id and progress == 'AwaitingConfirmation'):
                print("updating to lpr failed")
                db.collection("ParkingRequest").document(pid).collection('requests').document(key).update({"progress":"LprFailed"})
                break

    print("done")
    
    # if val = 0 stay in loop
    while(val == 0):
        val = GPIO.input(3)

GPIO.cleanup()

    # if(key != ""):
    #     print('timer started')
    #     # start a timer till val == 0
    #     oldtime = time()
    #     while(val == 0):
    #         val = GPIO.input(3)
    #
    #     print('timer ended')
    #     # find total time
    #     totaltime = time() - oldtime
    #     totaltime = totaltime / 3600 # convert to hours
    #
    #     # subtract 200 parkoins per hour
    #     doc = db.collection('ParkingUsers').document(key).collection('Coins').document('parKoin').get()
    #     balance = doc.to_dict()['amount']
    #     amount = str(balance - 200 * totaltime)
    #     docs = db.collection('ParkingUsers').document(key).collection('Coins').document('parKoin').update({'amount': amount})
    #
    #     # change inParking status
    #     docs = db.collection('ParkingUsers').where("lpn", "==", lpn).get()
    #     for doc in docs:
    #         if(uid == doc.id and progress == 'Confirmed'):
    #             db.collection("ParkingRequest").document(pid).collection('requests').document(key).update({"progress":"OldRequest"})
    #     print('done!')
    #
    # else:
    #     # handle when lpn not found in db
    #     print("user not found")
