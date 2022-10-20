import os

from flask import current_app, flash, session

def directory_count_and_size(directory):
    count = 0
    size = 0

    for root_dir, cur_dir, files in os.walk(directory):
        count += len(files)

        for file in files:
            filename = os.path.join(root_dir, file)
            size += os.path.getsize(filename)

    return count, size

def get_transfer_directory():
    transfer_dir = ""

    if "transfer_directory" in session:
        transfer_dir = session["transfer_directory"]

    if transfer_directory_set_in_config():
        transfer_dir = current_app.config["TRANSFER_DIRECTORY"]
        flash(f"Using transfer at {transfer_dir}", "warning")

    return transfer_dir

def transfer_directory_set_in_config():
    return "TRANSFER_DIRECTORY" in current_app.config and current_app.config["TRANSFER_DIRECTORY"] is not None
