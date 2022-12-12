import os
import shutil

from uploader.job import Job
from uploader.Metadata import DATAVERSE_METADATA_FILENAME, FORM_FILE_NAME, arc_metadata
from uploader.Navigator import permissions
from uploader.Transfer.helpers import potential_dir_name


class CreateTransferJob(Job):
    def run(self):
        super().begin("copy", self.params)

        # Copy transfer files to transfer source location
        self.params["destination"] = potential_dir_name(self.params["destination"])
        shutil.copytree(self.params["source"], self.params["destination"])

        # Create metadata directory if need be
        metadata_directory = os.path.join(self.params["destination"], "metadata")

        if not os.path.isdir(metadata_directory):
            os.mkdir(metadata_directory)

        # Move main metadata file, if it exists, to metadata directory
        main_metadata_filepath = os.path.join(
            self.params["destination"], DATAVERSE_METADATA_FILENAME
        )

        if os.path.isfile(main_metadata_filepath):
            shutil.copy(main_metadata_filepath, metadata_directory)
            os.remove(main_metadata_filepath)

        # Get file permission metadata, if it exists
        permission_file_path = os.path.join(
            self.params["destination"], permissions.PERMISSION_METADATA_FILENAME
        )

        if os.path.isfile(permission_file_path):
            # Load file permission metadata
            perms = permissions.FilePermissions(permission_file_path)
            perms.load()

        # Create archivematica metadata file
        metadata_dest_dir = os.path.join(self.params["destination"], "metadata")
        arc_metadata.create_metadata(
            self.params["form"], perms.permissions, metadata_dest_dir
        )

        # Remove working data files
        os.remove(os.path.join(self.params["destination"], FORM_FILE_NAME))
        os.remove(permission_file_path)

        super().end()
