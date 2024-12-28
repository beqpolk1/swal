from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://db:27017/"

mongoClient = MongoClient(app.config["MONGO_URI"])

@app.route('/')
def hello_world():
    return 'Hello World - this is Flasky McFlask Face<br />2'

@app.route('/dbtest')
def dbtest():
    mongoClient.admin.command('ping')
    return 'Connected to MongoDB version ' + mongoClient.server_info()["version"]

if __name__ == '__main__':
    app.run()