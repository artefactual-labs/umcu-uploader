import os
import yaml


# Attempt to load application configuration
app_config_filepath = "/etc/umcu-uploader.yaml"

if os.path.isfile(app_config_filepath):
    with open(app_config_filepath, "r") as stream:
        app_config = yaml.safe_load(stream)


class Config:
    # Be sure to set a secure secret key for production.
    SECRET_KEY = os.getenv("SECRET_KEY", "you-will-never-guess")

    DATA_DIRECTORY = os.getenv("DATA_DIRECTORY")
    TRANSFER_SOURCE_DIRECTORY = os.getenv("TRANSFER_SOURCE_DIRECTORY")
    DEPARTMENTS = {}

    DEBUG = os.getenv("DEBUG") == "True"
    TESTING = False


# Set departments configuration, if available
if "app_config" in locals() and "departments" in app_config:
    Config.DEPARTMENTS = app_config['departments']


CONFIGS = {"default": Config}
