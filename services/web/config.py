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

    DEFAULT_SEARCH_LIMIT = 10
    SEARCH_LIMIT_MAX = 100
    SEARCH_LIMIT_MIN = 1
    
    MAX_ARTIST_LENGTH = 255
    MAX_ALBUM_LENGTH = 500
    MAX_RELEASE_YEAR = 2150
    MIN_RELEASE_YEAR = 1800
    MAX_GENRE_LENGTH = 255
    VALID_INTEREST_LVL = [1, 2, 3]

    MIN_Q_LENGTH = 3
    MAX_Q_LENGTH = 255

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # Override with production values if needed