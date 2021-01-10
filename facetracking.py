import cv2
import numpy
import time
import statistics

# Load the cascade
cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')

# Get video from default device
cap = cv2.VideoCapture(0)

# Prep processing
startInterval = time.time()
countList = []


while (time.time() - 3 < startInterval):
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
    print(num)

    # Draw the rectangle around each face for testing
    for (x, y, w, h) in people:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Display
    cv2.imshow('img', img)

    # Stop if escape key is pressed
    if cv2.waitKey(1) == 27:
        break

result = statistics.mode(countList)
print(result)
    
# Release the VideoCapture object
cap.release()

#Destroy window showing video
cv2.destroyAllWindows()