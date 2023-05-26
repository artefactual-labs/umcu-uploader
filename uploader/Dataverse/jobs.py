import json
import os
import shutil
import tempfile
import time
from urllib.parse import urlparse

import py7zr
import tarfile
import zipfile
from pyDataverse.api import NativeApi
from pyDataverse.models import Dataset, Datafile
from pyDataverse.utils import read_file

from uploader.job import Job
from uploader.Dataverse.helpers import (
    download_aip,
    find_file_metadata,
    find_metadata_json_file,
    populate_dataverse_dir,
)
from uploader.Metadata import (
    DIVISIONS_FILE_PATH,
    DATAVERSE_METADATA_FILENAME,
    ARCHIVEMATICA_METADATA_FILENAME,
)
from uploader.Metadata.helpers import get_division_acronym
from uploader.Transfer.helpers import create_unique_dir_name


class CreateDataverseDatasetFromAipJob(Job):
    uuid: str = None
    config: dict = {}

    def run(self):
        self.begin("Exporting AIP to Dataverse")
        self.current_operation("Downloading AIP")

        local_filename = download_aip(self.uuid, self.config)

        if local_filename is None:
            self.error("Error downloading AIP")
            return

        # Extract AIP to working directory and delete compressed file
        self.current_operation("Extracting AIP")

        extract_directory = create_unique_dir_name(
            os.path.join(tempfile.gettempdir(), self.uuid)
        )
        os.mkdir(extract_directory)
        # Determine based on the file type how to open a file.
        if py7zr.is_7zfile(local_filename):
            archive = py7zr.SevenZipFile(local_filename)
        elif tarfile.is_tarfile(local_filename):
            archive = tarfile.open(local_filename)
        elif zipfile.is_zipfile(local_filename):
            archive = zipfile.open(local_filename)
        try:
            archive.extractall(path=extract_directory)
            archive.close()
        except (AttributeError, NameError) as E:
            self.error(f"{local_filename} is not a tar, 7zip or zip file.")

        os.unlink(local_filename)

        # Create and populate Dataverse package directory
        aip_subdir = os.listdir(extract_directory)[0]
        aip_directory = os.path.join(extract_directory, aip_subdir)
        dataverse_directory = os.path.join(extract_directory, "dataverse")
        os.mkdir(dataverse_directory)

        populate_dataverse_dir(self.uuid, aip_directory, dataverse_directory)

        # Assemble Dataverse base URL
        self.current_operation("Creating Dataverse dataset")

        if self.config["DEMO_MODE"]:
            server_url = self.config["DATAVERSE_DEMO_SERVER"]
        else:
            server_url = self.config["DATAVERSE_SERVER"]

        url_parts = urlparse(server_url)
        base_url = f"{url_parts.scheme}://{url_parts.hostname}"

        # Create Dataverse dataset
        dv_metadata_filepath = find_metadata_json_file(
            self.uuid, aip_directory, f"/{DATAVERSE_METADATA_FILENAME}"
        )

        if dv_metadata_filepath is None:
            self.error("AIP contains no Dataverse metadata")
            return

        metadata_filepath = os.path.join(aip_directory, "data", dv_metadata_filepath)

        api = NativeApi(base_url, self.config["DATAVERSE_API_KEY"])
        ds = Dataset()
        # Add in the the aip uuid to the dataverse metadata
        with open(metadata_filepath, "r+") as dv_json_file:
            dv_json = json.load(dv_json_file)
            dv_json["datasetVersion"]["metadataBlocks"]["citation"]["fields"].append(
                {
                    "typeName": "dataSources",
                    "multiple": True,
                    "typeClass": "primitive",
                    "value": [
                        self.uuid,
                    ],
                }
            )

            # Make slight metadata change to accord with pyDataverse client
            if "license" in dv_json["datasetVersion"]:
                dv_json["datasetVersion"]["license"] = dv_json["datasetVersion"][
                    "license"
                ]["name"]

            ds.from_json(json.dumps(dv_json))

        # Get the division acronym from the metadata in the AIP
        arc_metadata_filepath = os.path.join(
            aip_directory,
            "data",
            find_metadata_json_file(
                self.uuid, aip_directory, f"/{ARCHIVEMATICA_METADATA_FILENAME}"
            ),
        )

        # Load the JSON into an array of metadata
        with open(arc_metadata_filepath) as file:
            arc_metadata_array = json.load(file)

        # Loop through the array to find division
        division = None

        for arc_metadata_dict in arc_metadata_array:
            # If the dictionary is objects then take note of the division acronym
            if arc_metadata_dict["filename"] == "objects/":
                division = arc_metadata_dict["other.division"]

        if division is None:
            self.error("Unable to find division in metadata")
            return

        # Find division acronym
        division_acronym = get_division_acronym(DIVISIONS_FILE_PATH, division)

        if division_acronym == "No acroynm found":
            self.error("Unable to find acronym for division")
            return

        # Create the Dataverse dataset using the acronym
        resp = api.create_dataset(division_acronym, ds.json(validate=False))
        response_data = resp.json()

        if response_data["status"] != "OK":
            self.error(
                f"Error creating Dataverse dataset: {response_data['message']}",
                resp.status_code,
            )
            return

        ds_pid = response_data["data"]["persistentId"]

        # Get file metadata stored with AIP
        aip_metadata_relative_path = find_metadata_json_file(
            self.uuid, aip_directory, f"/{ARCHIVEMATICA_METADATA_FILENAME}"
        )

        aip_metadata_filepath = os.path.join(
            aip_directory, "data", aip_metadata_relative_path
        )

        with open(aip_metadata_filepath) as file:
            aip_metadata_array = json.load(file)

        # Upload each file to Dataverse
        self.current_operation("Uploading files to Dataverse")

        for root, dirs, files in os.walk(dataverse_directory, topdown=False):
            for name in files:
                subdir = root[len(dataverse_directory) + 1 :]

                df = Datafile()
                df_filename = os.path.join(root, name)

                # Default file metadata
                dv_file_metadata = {
                    "pid": ds_pid,
                    "filename": df_filename,
                    "directoryLabel": subdir,
                }

                # Set restriction status, if applicable
                relative_filepath = os.path.join(subdir, os.path.basename(df_filename))
                file_metadata = find_file_metadata(
                    aip_metadata_array, relative_filepath
                )

                dv_file_metadata["restrict"] = (
                    file_metadata is not None
                    and file_metadata["dc.accessRights"] == "restricted"
                )

                df.set(dv_file_metadata)
                resp = api.upload_datafile(ds_pid, df_filename, df.json())

                time.sleep(1)

        # Remove working files
        self.current_operation("Deleting working files")
        shutil.rmtree(extract_directory)

        self.end()
