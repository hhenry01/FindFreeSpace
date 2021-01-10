import pymongo
from pymongo import MongoClient
import smtplib, ssl

port = 465
password = "findfree.space.nwhacks2021"

context = ssl.create_default_context

with smtplib.SMTP_SSL("smtp.gmail.com", port, context = context) as server: 
    server.login("FFSnwhacks@gmail.com", password)

cluster = MongoClient("mongodb+srv://pogchamp:poggers@findfreespace-web.34zzj.mongodb.net/findfreespace?retryWrites=true&w=majority")
db = cluster["findfreespace"]
cameras = db["cameras"]
buildings = db["buildings"]