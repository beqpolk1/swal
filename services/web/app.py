from flask import Flask, redirect, url_for
from pymongo import MongoClient
from modules import index, add_entry
import os

def create_app():
    ################################################
    # app startup/config
    ################################################

    app = Flask(__name__)

    # Load config based on environment variable
    config_name = os.getenv("FLASK_CONFIG", "DevelopmentConfig")
    app.config.from_object(f"config.{config_name}")

    ################################################
    # basic/utility routes
    ################################################

    @app.route('/media/<filename>')
    def media():
        return

    @app.route('/dbtest')
    def dbtest():
        mongoClient = MongoClient(app.config["MONGO_CONN_STR"], serverSelectionTimeoutMS=app.config["MONGO_CONN_TIMEOUT"])
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

    app.add_url_rule('/', 'index', index, methods = ['GET'])
    app.add_url_rule('/add_entry/<string:mode>', 'add_entry', add_entry, methods = ['GET', 'POST'])

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()