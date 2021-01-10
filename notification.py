import pymongo
from pymongo import MongoClient
import smtplib, ssl, numpy, email

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
            validEmptyRoomCameras = []
            for camera in listEmptyRooms:
                if str(camera["_id"]) in person["requestedRoomIDs"]:
                    validEmptyRoomCameras.append(camera)
            emailQueue.update({person["_id"]: tuple(validEmptyRoomCameras)})

    for person in emailQueue.keys():
        emptyRooms = emailQueue[person] # list containing all cameras requested by client
        message = "The following study rooms are available:"
        for camera in emptyRooms:
            message += "\n" + str(camera["building"]) + "-" + str(camera["room_num"])
        currentClient = notifications.find_one({"_id": person})
        sendEmail(message, currentClient["email"])
        notifications.update_one({"_id": currentClient["_id"]}, {"$set": {"searching": False}})
