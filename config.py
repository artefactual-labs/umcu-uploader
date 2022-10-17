import os

class Config:
    # Be sure to set a secure secret key for production.
    SECRET_KEY = os.getenv("SECRET_KEY", "you-will-never-guess")

    DEBUG = False
    TESTING = False

CONFIGS = {"default": Config}
