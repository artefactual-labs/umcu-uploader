import csv
import json
import os

from uploader.Transfer import helpers


from uploader.Metadata import arc_metadata
from uploader.Metadata import Formdata
PERMISSION_METADATA_FILENAME = "permissions.json"


class FilePermissions:
    filepath = ""  # Path to permissions JSON file
    permissions = {}  # Permissions data

    def __init__(self, filepath=None):
        self.filepath = filepath

    def load(self):
        # Read permissions from JSON if applicable
        try:
            with open(self.filepath) as data:
                # TODO: send permissions to the create archivematica metadata function
                self.permissions = arc_metadata.create_archivematica_metadata(data)
        except FileNotFoundError():       
                self.permissions = {}

    def copy_from_dict(self, permissions):
        self.permissions = permissions.copy()

    def save(self):
        # Write permissions to JSON
        with open(self.filepath, "w") as file:
            file.write(arc_metadata.create_archivematica_metadata(self.permissions))

    def set(self, entry_path, permission):
        # Remove any blank permissions
        if permission == "" and entry_path in self.permissions:
            del self.permissions[entry_path]
        elif permission != "" and permission is not None:
            self.permissions[entry_path] = permission

    def get(self, entry_path):
        if entry_path in self.permissions:
            return self.permissions[entry_path]

        return None

    # Set permissions for all descendants of an entry
    def set_descendant_perms(self, entry_path, permission):
        files = helpers.get_all_filepaths_in_directory(entry_path, False)

        for filepath in files:
            if filepath.startswith(entry_path + "/"):
                self.set(filepath, permission)

    # Write permissions to an Archivematica metadata CSV file
    def write_permissions_to_csv(self, transfer_dir, destination_csv_file_path):
        permission_filepath = os.path.join(transfer_dir, PERMISSION_METADATA_FILENAME)

        with open(destination_csv_file_path, "w", newline="") as csvfile:
            fieldnames = ["filename", "dc.rights"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header
            writer.writeheader()

            # Write rows in order
            for filename in sorted(self.permissions.keys()):
                if self.permissions[filename] != "":
                    filename_fixed = filename.replace(transfer_dir, "objects")
                    writer.writerow(
                        {
                            "filename": filename_fixed,
                            "dc.rights": self.permissions[filename].capitalize(),
                        }
                    )
