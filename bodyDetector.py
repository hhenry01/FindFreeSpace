import cv2
import numpy
import time
import statistics
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://pogchamp:poggers@findfreespace-web.34zzj.mongodb.net/findfreespace?retryWrites=true&w=majority")
db = cluster["findfreespace"]
collection = db["cameras"]

# Load the cascade
cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')

# Get video from default device
cap = cv2.VideoCapture(0)

id = 101
room_num = 101
floor = 1

stop = False

try:
    collection.insert_one({"_id": id, "room_num": room_num, "floor": floor})
except:
    pass

while True:
    # Prep processing
    startInterval = time.time()
    countList = []
    
    while (time.time() - 30 < startInterval):
        # Read the frame
        _, img = cap.read()

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect 
        people = cascade.detectMultiScale(gray, 1.1, 4) #color, scalefactor, min neighbors

        # Process 
        num = 0
        if type(people) is numpy.ndarray:
            for x in people:
                num = num + 1
        countList.append(num)

        # Draw the rectangle around each face for testing
        for (x, y, w, h) in people:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Display
        cv2.imshow('img', img)

        # Stop if escape key is pressed
        if cv2.waitKey(1) == 27:
            stop = True
            break

    result = statistics.mode(countList)
    

    collection.update_one({"_id": id}, {"$set": {"num_people": result}})

    if stop or cv2.waitKey(1) == 27: 
        break
    
    print(result)
    
# Release the VideoCapture object
cap.release()

#Destroy window showing video
cv2.destroyAllWindows()
