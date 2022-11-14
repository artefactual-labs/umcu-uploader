import os

class Config:
    # Be sure to set a secure secret key for production.
    SECRET_KEY = os.getenv("SECRET_KEY", "you-will-never-guess")

    DATA_DIRECTORY = os.getenv("DATA_DIRECTORY")
    TRANSFER_SOURCE_DIRECTORY = os.getenv("TRANSFER_SOURCE_DIRECTORY")
    DEBUG = os.getenv("DEBUG") == "True"
    TESTING = False

CONFIGS = {"default": Config}
