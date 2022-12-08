import os
import yaml


# Specifiy config fields and defaults
config_fields = {
    "host": "0.0.0.0",
    "port": "5000",
    "debug": False,
    "secret_key": "you-shall-not-pass🧙<200d>♂️",
    "data_directory": None,
    "transfer_source_directory": None,
    "dataverse_server": "https://dataverse.nl/dataverse/",
    "dataverse_demo_server": "https://demo.dataverse.nl/dataverse/",
    "demo_mode": True,
    "depositor_name": "ANON",
    "divisions": {},
}

# Initialize configuration
class Config:
    TESTING = False


# Set default config values
for field_name in config_fields.keys():
    setattr(Config, field_name.upper(), config_fields[field_name])

# Populate config with values from YAML file, if available
config_filepath = "/etc/umcu-uploader.yaml"

try:
    with open(config_filepath, "r") as stream:
        settings_config = yaml.safe_load(stream)

    # Overwrite defaults with values from config file, if they've been set
    for field_name in config_fields.keys():
        if field_name in settings_config:
            setattr(Config, field_name.upper(), settings_config[field_name])

except (FileNotFoundError, IOError):
    print(
        f"*** WARNING: {config_filepath} does not exist, using default configuration (see README.md). ***\n"
    )

# Expose configuration values as module constant
CONFIGS = {"default": Config}
