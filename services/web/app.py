from flask import Flask, redirect, url_for, render_template
from pymongo import MongoClient

from modules import index

################################################
# app startup/config
################################################

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://db:27017/"

mongoClient = MongoClient(app.config["MONGO_URI"])

################################################
# basic/utility routes
################################################

@app.route('/media/<filename>')
def media():
    return

@app.route('/dbtest')
def dbtest():
    mongoClient.admin.command('ping')
    return 'Connected to MongoDB version ' + mongoClient.server_info()["version"]

@app.route('/statictest')
def statictest():
    return redirect(url_for('static', filename = 'test.txt'))

@app.route('/mediatest')
def mediatest():
    return redirect(url_for('media', filename = 'img/media_test.jpg'))

################################################
# external module routes
################################################

app.add_url_rule('/', 'index', index)


if __name__ == '__main__':
    app.run()