from uploader.configutil import set_config_from_yaml


# Specifiy config fields and defaults
config_fields = {
    "host": "0.0.0.0",
    "port": "5000",
    "debug": False,
    "secret_key": "you-shall-not-pass🧙<200d>♂️",
    "data_directory": None,
    "transfer_source_directory": None,
    "storage_server_url": None,
    "storage_server_user": None,
    "storage_server_api_key": None,
    "storage_server_basic_auth_user": None,
    "storage_server_basic_auth_password": None,
    "dataverse_server": "https://dataverse.nl/dataverse/",
    "dataverse_demo_server": "https://demo.dataverse.nl/dataverse/",
    "dataverse_api_key": None,
    "demo_mode": True,
    "depositor_name": "ANON",
    "divisions": {},
}

# Initialize configuration
class Config:
    TESTING = False


# Populate config with values from YAML file, if available
config_filepath = "/etc/umcu-uploader.yaml"

try:
    set_config_from_yaml(Config, config_fields, config_filepath)

except (FileNotFoundError, IOError):
    print(
        f"*** WARNING: {config_filepath} does not exist, using default configuration (see README.md). ***\n"
    )

# Expose configuration values as module constant
CONFIGS = {"default": Config}
