from flask import Flask, redirect, url_for
from pymongo import MongoClient

################################################
# app startup/config
################################################

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://db:27017/"
app.config["MEDIA_IMG"] = "img/"

mongoClient = MongoClient(app.config["MONGO_URI"])

################################################
# basic/utility routes
################################################

@app.route('/media/<filename>')
def media():
    return

@app.route('/')
def hello_world():
    return 'Hello World - this is Flasky McFlask Face<br />2'

@app.route('/dbtest')
def dbtest():
    mongoClient.admin.command('ping')
    return 'Connected to MongoDB version ' + mongoClient.server_info()["version"]

@app.route('/statictest')
def statictest():
    return redirect(url_for('static', filename='test.txt'))

@app.route('/mediatest')
def mediatest():
    return redirect(url_for('media', filename = app.config["MEDIA_IMG"] + 'media_test.jpg'))

################################################
# external module routes
################################################

if __name__ == '__main__':
    app.run()