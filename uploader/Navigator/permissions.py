import csv
import json
import os


PERMISSION_METADATA_FILENAME = "permissions.json"


def read_permissions(permission_file_path):
    # Read permissions from JSON if applicable
    try:
        with open(permission_file_path) as data:
            permissions = json.load(data)
    except FileNotFoundError:
        permissions = {}

    return permissions


def set_permission(permission_file_path, entry_path, permission):
    permissions = read_permissions(permission_file_path)

    permissions[entry_path] = permission

    # Write permissions to JSON
    file = open(permission_file_path, "w")
    file.write(json.dumps(permissions))
    file.close()


def write_permissions_to_csv(transfer_dir, destination_csv_file_path):
    permission_filepath = os.path.join(transfer_dir, PERMISSION_METADATA_FILENAME)
    permissions = read_permissions(permission_filepath)

    with open(destination_csv_file_path, "w", newline="") as csvfile:
        fieldnames = ["filename", "dc.rights"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write rows in order
        for filename in sorted(permissions.keys()):
            if permissions[filename] != "":
                filename_fixed = filename.replace(transfer_dir, "objects")
                writer.writerow(
                    {"filename": filename_fixed, "dc.rights": permissions[filename]}
                )
