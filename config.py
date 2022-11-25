import os
import yaml


# Attempt to load admin configuration
admin_config_filepath = "/etc/umcu-uploader.yaml"

if os.path.isfile(admin_config_filepath):
    with open(admin_config_filepath, "r") as stream:
        admin_config = yaml.safe_load(stream)


class Config:
    # Be sure to set a secure secret key for production.
    SECRET_KEY = os.getenv("SECRET_KEY", "you-will-never-guess")

    DATA_DIRECTORY = os.getenv("DATA_DIRECTORY")
    TRANSFER_SOURCE_DIRECTORY = os.getenv("TRANSFER_SOURCE_DIRECTORY")
    DIVISIONS = {} # Populated by admin configuration

    DEBUG = os.getenv("DEBUG") == "True"
    TESTING = False


# Set division configuration, if available
if "admin_config" in locals() and "divisions" in admin_config:
    # Data structure is:
    # {<division ID>: {"name": <division name>, "transfer_source_directory": <transfer source dir.>}}
    Config.DIVISIONS = admin_config['divisions']


CONFIGS = {"default": Config}
