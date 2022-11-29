import os
import shutil
import tempfile
import time
from urllib.parse import urlparse

import metsrw
from pyunpack import Archive
from pyDataverse.api import NativeApi
from pyDataverse.models import Dataset, Datafile
from pyDataverse.utils import read_file

from uploader.job import Job
from uploader.Dataverse.helpers import (
    download_aip,
    populate_dataverse_dir,
    find_dv_metadata_json_file,
)
from uploader.Transfer.helpers import potential_dir_name


class CreateDataverseDatasetFromAipJob(Job):
    def run(self):
        super().begin("dataverse", self.params)

        uuid = self.params["uuid"]

        local_filename = download_aip(uuid, self.params["config"])

        if local_filename is None:
            self.error("Error downloading AIP")
            return

        # Extract AIP to working directory and delete compressed file
        extract_directory = potential_dir_name(
            os.path.join(tempfile.gettempdir(), uuid)
        )
        os.mkdir(extract_directory)

        Archive(local_filename).extractall(extract_directory)
        os.unlink(local_filename)

        # Create and populate Dataverse package directory
        aip_subdir = os.listdir(extract_directory)[0]
        aip_directory = os.path.join(extract_directory, aip_subdir)
        dataverse_directory = os.path.join(extract_directory, "dataverse")
        os.mkdir(dataverse_directory)

        populate_dataverse_dir(uuid, aip_directory, dataverse_directory)

        # Assemble Dataverse base URL
        if self.params["config"]["DEMO_MODE"]:
            server_url = self.params["config"]["DATAVERSE_DEMO_SERVER"]
        else:
            server_url = self.params["config"]["DATAVERSE_SERVER"]

        url_parts = urlparse(server_url)
        base_url = f"{url_parts.scheme}://{url_parts.hostname}"

        # Create Dataverse dataset
        dv_metadata_filepath = find_dv_metadata_json_file(uuid, aip_directory)

        if dv_metadata_filepath is None:
            self.error("AIP contains no Dataverse metadata")
            return

        metadata_filepath = os.path.join(
            aip_directory, "data", find_dv_metadata_json_file(uuid, aip_directory)
        )

        api = NativeApi(base_url, self.params["config"]["DATAVERSE_API_KEY"])
        ds = Dataset()
        ds.from_json(read_file(metadata_filepath))

        # Note: dataverse alias is hardcoded for now
        resp = api.create_dataset("umculab", ds.json())
        response_data = resp.json()

        if response_data["status"] != "OK":
            self.error("Error creating Dataverse dataset", resp.status_code)
            return

        ds_pid = response_data["data"]["persistentId"]

        # Upload each file
        for root, dirs, files in os.walk(dataverse_directory, topdown=False):
            for name in files:
                subdir = root[len(dataverse_directory) + 1 :]

                df = Datafile()
                df_filename = os.path.join(root, name)
                df.set(
                    {"pid": ds_pid, "filename": df_filename, "directoryLabel": subdir}
                )
                resp = api.upload_datafile(ds_pid, df_filename, df.json())

                time.sleep(1)

        super().end()
