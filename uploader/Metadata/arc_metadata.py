import json
import os
from config import Config

from uploader.Metadata import ARCHIVEMATICA_METADATA_FILENAME


def create_metadata(form: dict, permissions: dict, transfer_dir: str, destination_dir: str) -> None:
    """create archivematica metadata file"""

    if not Config.DEMO_MODE:
        server = Config.DATAVERSE_SERVER
    else:
        server = Config.DATAVERSE_DEMO_SERVER

    if form is None or permissions is None:
        raise TypeError(
            "Expected form and permissions to be set,\ngot form: %s \n\npermissions: %s"
            % (form, permissions)
        )
    root: str = "objects"
    metadata_list = [] 
    for filename in permissions.keys():
        # Remove transfer directory from filepath and prepend with "objects"
        relative_path = os.path.join("objects", filename[len(transfer_dir) + 1:])

        metadata_list.append({
            "filename": relative_path,
            "dc.accesRights": permissions[filename],
        })

    keyword_list = form["keywords"]
    keyword_list.append(form["subject"])
    root_metadata = {
        "filename": 'objects/',
        "dc.title": form["title"],
        "dc.creator": form["author"],
        "dc.description": form["description"],
        "dc.subject": keyword_list,
        "dc.publisher": server+form['divisionAcronym'],
        "dc.dateSubmitted": form["dateOfDeposit"],
        "dc.language": "English",
        "dc.temporal": form["daterangeStart"],
        "other.researchProjectEndDate": form["researchEndDate"],
        "dc.coverage": f"start={form['researchEndDate']}, end={form['retention']}",
        "dc.rights": form["license"],
        "dc.type": form["kindOfData"],
        "dc.isReferencedBy": form["publication"],
        "other.researchType": form["researchType"],
        "other.depositor": form["depositor"],
        "other.contributor": form["contributor"],
        "other.contact": form["contactName"],
        "other.division": form["division"],
    }

    metadata_list.append(root_metadata)
    metadata_filepath = os.path.join(destination_dir, ARCHIVEMATICA_METADATA_FILENAME)
    with open(metadata_filepath, "w") as f:
        json.dump(metadata_list, f, indent=4)
    return None
