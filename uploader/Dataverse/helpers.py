# -*- coding: utf-8 -*-

import os
import re
import shutil
import tempfile

import metsrw
import requests
from requests.auth import HTTPBasicAuth


def get_basic_auth_config(config):
    auth = None

    ss_http_user = config["STORAGE_SERVER_BASIC_AUTH_USER"]
    ss_http_password = config["STORAGE_SERVER_BASIC_AUTH_PASSWORD"]

    if ss_http_user is not None and ss_http_password is not None:
        auth = HTTPBasicAuth(ss_http_user, ss_http_password)

    return auth


def download_aip(uuid, config):
    # Required parameters for storage server access
    url = f"{config['STORAGE_SERVER_URL']}/api/v2/file/{uuid}/download/"

    params = {
        "username": config["STORAGE_SERVER_USER"],
        "api_key": config["STORAGE_SERVER_API_KEY"],
    }

    # Make request to storage server
    response = requests.get(
        url, params=params, auth=get_basic_auth_config(config), stream=True
    )

    if response.status_code == 200:
        # Assemble filename
        try:
            local_filename = re.findall(
                'filename="(.+)"', response.headers["content-disposition"]
            )[0]
        except KeyError:
            # NOTE: assuming that packages are always stored as .7z
            local_filename = "package-{}.7z".format(uuid)

        local_filename = os.path.join(tempfile.gettempdir(), local_filename)

        # Download AIP
        with open(local_filename, "wb") as package:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    package.write(chunk)

        return local_filename

    return None


def dmdtext_access_rights(dmdsec) -> str:
    dmdele = dmdsec.serialize()
    dmdele = dmdele.find(".//dc:accessRights", namespaces=metsrw.utils.NAMESPACES)
    if dmdele is not None:
        return dmdele.text
    return "No access condition found"


def create_dips(aipfile, dip_directory, dataverse_directory, file_subpath):
    source_path = os.path.join(dataverse_directory, "data", "objects", file_subpath)
    dest_path = os.path.join(dip_directory, file_subpath)
    dest_path_components = os.path.split(dest_path)
    # Create subdir(s) if necessary
    if not os.path.isdir(dest_path_components[0]):
        os.makedirs(dest_path_components[0])
    # Copy the aipfile if it does not have private access
    for dmdsec in aipfile.dmdsecs:
        dmdsec.access_condition = dmdtext_access_rights(dmdsec)
        if dmdsec.access_condition in ["public", "restricted"]:
            shutil.copy(source_path, dest_path_components[0])


def populate_dataverse_dir(uuid, aip_directory, dataverse_directory, dip_directory):
    mets_filename = f"METS.{uuid}.xml"
    mets_filepath = os.path.join(aip_directory, "data", mets_filename)

    mets = metsrw.METSDocument.fromfile(mets_filepath)
    files = mets.all_files()
    # Copy files to Dataverse directory
    for aipfile in files:
        if aipfile.type == "Item":
            file_subpath = aipfile.path[8:]

            # Assemble destination subdirectory and path
            source_path = os.path.join(aip_directory, "data", "objects", file_subpath)

            dest_path = os.path.join(dip_directory, file_subpath)
            dest_path_components = os.path.split(dest_path)

            # Create subdir(s) if necessary
            if not os.path.isdir(dest_path_components[0]):
                os.makedirs(dest_path_components[0])

            # Copy file
            shutil.copy(source_path, dest_path_components[0])

            create_dips(aipfile, dataverse_directory, aip_directory, file_subpath)


def find_metadata_json_file(uuid, aip_directory, file):
    mets_filename = f"METS.{uuid}.xml"
    mets_filepath = os.path.join(aip_directory, "data", mets_filename)

    mets = metsrw.METSDocument.fromfile(mets_filepath)
    files = mets.all_files()

    for aipfile in files:
        if (
            aipfile.type == "Item"
            and aipfile.get_path()
            and aipfile.get_path().endswith(file)
        ):
            return aipfile.get_path()


def find_file_metadata(metadata, file_rel_path):
    for item in metadata:
        if file_rel_path == item["filename"][8:]:
            return item
