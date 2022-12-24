import os
import yaml

CONFIG_FILE_LOCATIONS = [".config.yaml", "/etc/umcu-uploader.yaml"]


def get_config_file():
    # Return first file found in possible config file locations
    for config_file in CONFIG_FILE_LOCATIONS:
        if os.path.isfile(config_file):
            return config_file

    # Return first possible config file in list as suggestion
    return config_file[0]


def set_config_from_yaml(config, config_fields, config_filepath):
    # Set default config values
    for field_name in config_fields.keys():
        setattr(config, field_name.upper(), config_fields[field_name])

    # Load config from YAML
    with open(config_filepath, "r") as stream:
        settings_config = yaml.safe_load(stream)

    # Overwrite defaults with values from config file, if they've been set
    for field_name in config_fields.keys():
        if field_name in settings_config:
            setattr(config, field_name.upper(), settings_config[field_name])


def config_subset_dict(config, settings):
    subset = {}

    for setting in settings:
        subset[setting] = config[setting]

    return subset
