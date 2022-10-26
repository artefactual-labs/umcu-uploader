import os

class Config:
    # Be sure to set a secure secret key for production.
    SECRET_KEY = os.getenv("SECRET_KEY", "you-will-never-guess")

    TRANSFER_DIRECTORY = os.getenv("DATA_DIRECTORY")

    DEBUG = False
    TESTING = False

CONFIGS = {"default": Config}
