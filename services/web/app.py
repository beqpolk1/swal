from flask import Flask, redirect, url_for
from pymongo import MongoClient
from modules import index, add_entry, entries
import os

def create_app():
    ################################################
    # app startup/config
    ################################################

    app = Flask(__name__)

    # Load config based on environment variable
    config_name = os.getenv("FLASK_CONFIG", "DevelopmentConfig")
    app.config.from_object(f"config.{config_name}")

    @app.context_processor
    def inject_config():
        return {
            'MEDIA_IMG_DIR': app.config['MEDIA_IMG_DIR'],
            'JS_STATIC_DIR': app.config['JS_STATIC_DIR'],
            'IMG_STATIC_DIR': app.config['IMG_STATIC_DIR'],
            'CSS_STATIC_DIR': app.config['CSS_STATIC_DIR'],
            'LOGO_IMG': app.config['LOGO_IMG']
        }

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
        return redirect(url_for('media', filename = app.config['MEDIA_IMG_DIR'] + '/media_test.jpg'))

    ################################################
    # external module routes
    ################################################

    app.add_url_rule('/', 'index', index, methods = ['GET'])
    app.add_url_rule('/add_entry/<string:mode>', 'add_entry', add_entry, methods = ['GET', 'POST'])
    app.add_url_rule('/entries/', 'entries', entries, methods = ['GET'])
    app.add_url_rule('/entries/<string:_id>/', 'entries', entries, methods = ['GET'])

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()