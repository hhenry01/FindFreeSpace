import pymongo
from pymongo import MongoClient
import smtplib, ssl, numpy, email, time

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

NOTIFICATION_COOLDOWN = 10 #min number of seconds between email notifications. Right now 10s for testing

cluster = MongoClient("mongodb+srv://pogchamp:poggers@findfreespace-web.34zzj.mongodb.net/findfreespace?retryWrites=true&w=majority")
db = cluster["findfreespace"]
cameras = db["cameras"]
buildings = db["buildings"]
notifications = db["notifications"]

def sendEmail(message, receiver_email):
    sender_email = "FFSnwhacks@gmail.com"
    password = "findfree.space.nwhacks2021"
    smtp_server = "smtp.gmail.com"
    port = 465

    finalMessage = MIMEMultipart()
    finalMessage["From"] = sender_email
    finalMessage["To"] = receiver_email
    finalMessage["Subject"] = "Study rooms available!"
    finalMessage.attach(MIMEText(message, "plain"))

    text = finalMessage.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context = context) as server: 
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

while True:
    listEmptyRooms = []
    for camera in cameras.find({}):
        if camera["num_people"] == 0:
            listEmptyRooms.append(camera)
    
    emailQueue = {}
    for person in notifications.find({}):
        if person["searching"] == True:
            print(time.time())
            validEmptyRoomCameras = []
            for camera in listEmptyRooms:
                if str(camera["_id"]) in person["requestedRoomIDs"]:
                    validEmptyRoomCameras.append(camera)
            emailQueue.update({person["_id"]: tuple(validEmptyRoomCameras)})
        else:
            if person["cooldown"] <= time.time():   # check to see if timeout is done
                notifications.update_one({"_id": person["_id"]}, {"$set": {"searching": True}})

    for person in emailQueue.keys():
        emptyRooms = emailQueue[person] # list containing all cameras requested by client
        message = "The following study rooms are available:"
        for camera in emptyRooms:
            building = camera["building"]
            building = building.capitalize()
            message += "\n" + building + "-" + str(camera["room_num"])
        currentClient = notifications.find_one({"_id": person})
        sendEmail(message, currentClient["email"])
        notifications.update_one({"_id": currentClient["_id"]}, {"$set": {"searching": False}})
        cooldown = time.time() + NOTIFICATION_COOLDOWN
        notifications.update_one({"_id": currentClient["_id"]}, {"$set": {"cooldown": cooldown}})
        ## set user timeout to specified time, e.g. 30 min or 1 hour - "$set": {"cooldown": time.time() + 1800}
