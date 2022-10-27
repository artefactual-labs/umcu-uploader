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

            # If a directory's permission has been set then delete any child permissions
            if os.path.isdir(entry_path):
                self.unset_permissions_of_descendants(entry_path)

    def get(self, entry_path):
        if entry_path in self.permissions:
            return self.permissions[entry_path]

        return None

    # Working through a directory and its ancestors, return the first permission
    # found.
    def get_inherited_permission_of_directory(self, entry_path):
        # Make sure function is being run on a directory
        if not os.path.isdir(entry_path):
            raise Exception("Entry path must be a directory.")

        # Return first permission found
        if entry_path in self.permissions:
            return self.permissions[entry_path]

        # If parent isn't root then recurse
        parent_directory_path = os.path.dirname(entry_path)

        if parent_directory_path != "/":
            return self.get_inherited_permission_of_directory(parent_directory_path)

        # No permission was found
        return None

    # Unset permissions for all descendants of an entry
    def unset_permissions_of_descendants(self, entry_path):
        keys = list(self.permissions.keys())
        for path in keys:
            if path.startswith(entry_path + "/"):
                del self.permissions[path]

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
