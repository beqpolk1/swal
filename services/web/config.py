class Config:
    MONGO_CONN_STR = "mongodb://mongoadmin:secret@db:27017/"
    MONGO_CONN_TIMEOUT = 2000
    FTP_SERVER_NAME = "nginx"
    FTP_USERNAME = "swal_image"
    FTP_PASSWORD = "swallowth3p4ssword"
    
    ARTIST_LENGTH_LIMIT = 255

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # Override with production values if needed