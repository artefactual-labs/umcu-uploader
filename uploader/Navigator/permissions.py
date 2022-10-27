import csv
import json
import os


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
                self.permissions = json.load(data)
        except FileNotFoundError:
            self.permissions = {}

    def copy_from_dict(self, permissions):
        self.permissions = permissions.copy()

    def save(self):
        # Write permissions to JSON
        file = open(self.filepath, "w")
        file.write(json.dumps(self.permissions))
        file.close()

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
