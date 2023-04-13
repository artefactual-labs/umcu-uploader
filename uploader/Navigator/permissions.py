import csv
import json
import os

from uploader.Transfer import helpers


PERMISSION_METADATA_FILENAME = "permissions.json"


class FilePermissions:
    def __init__(self, filepath=None):
        self.filepath = filepath  # Path to permissions JSON file
        self.permissions = {}  # Permissions data

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

    # Set permissions for all descendants of an entry
    def set_descendant_perms(self, entry_path, permission):
        files = helpers.get_all_filepaths_in_directory(entry_path, False)

        for filepath in files:
            if filepath.startswith(entry_path + "/"):
                self.set(filepath, permission)
