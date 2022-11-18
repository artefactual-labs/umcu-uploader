import os
import tempfile

from flask import current_app, flash, session

def directory_count_and_size(directory):
    count = 0
    size = 0

    for root_dir, cur_dir, files in os.walk(directory):
        count += len(files)

        for file in files:
            filename = os.path.join(root_dir, file)

            # Skip symlinks
            if os.path.isfile(filename):
                size += os.path.getsize(filename)

    return count, size

def get_data_directory():
    if data_directory_set_in_config():
        return current_app.config["DATA_DIRECTORY"]

    return tempfile.gettempdir()

def get_transfer_directory():
    transfer_dir = ""

    if "transfer_directory" in session:
        transfer_dir = session["transfer_directory"]

    return transfer_dir

def data_directory_set_in_config():
    return "DATA_DIRECTORY" in current_app.config and current_app.config["DATA_DIRECTORY"] is not None

def get_all_filepaths_in_directory(directory, trim_root=True):
    files = []

    for root, _, dir_files in os.walk(directory, topdown=False):
        for name in dir_files:
            if trim_root:
                files.append(os.path.join(root.replace(directory, ''), name))
            else:
                files.append(os.path.join(root, name))

    return files

def potential_dir_name(directory_path):
    potential_path = directory_path
    padding_counter = 1

    while os.path.exists(potential_path):
        potential_path = directory_path + '_' + str(padding_counter)

        padding_counter += 1

    return potential_path
