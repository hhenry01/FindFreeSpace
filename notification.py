import pymongo
from pymongo import MongoClient
import smtplib, ssl

smtp_server = "smtp.gmail.com"
port = 465
sender_email = "FFSnwhacks@gmail.com"
receiver_email = "FFSnwhacks@gmail.com"
password = "findfree.space.nwhacks2021"
message = """\
    Subject: Hi there

    This message is sent from Python."""

context = ssl.create_default_context()

cluster = MongoClient("mongodb+srv://pogchamp:poggers@findfreespace-web.34zzj.mongodb.net/findfreespace?retryWrites=true&w=majority")
db = cluster["findfreespace"]
cameras = db["cameras"]
buildings = db["buildings"]

with smtplib.SMTP_SSL("smtp.gmail.com", port, context = context) as server: 
    server.login("FFSnwhacks@gmail.com", password)
    server.sendmail(sender_email, receiver_email, message)