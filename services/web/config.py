class Config:
    MEDIA_IMG_DIR = "img"
    JS_STATIC_DIR = "js"
    IMG_STATIC_DIR = "img"
    CSS_STATIC_DIR = "css"

    LOGO_IMG = "swallow_small.jpg"
    
    MONGO_CONN_STR = "mongodb://mongoadmin:secret@db:27017/"
    MONGO_CONN_TIMEOUT = 2000
    MONGO_DB_NAME = "swal"
    MONGO_ENTRIES_COLL = "entries"

    FTP_SERVER_NAME = "nginx"
    FTP_USERNAME = "swal_image"
    FTP_PASSWORD = "swallowth3p4ssword"
    FTP_IMG_DIR = "img"
    
    ARTIST_LENGTH_LIMIT = 255

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # Override with production values if needed