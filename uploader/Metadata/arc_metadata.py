import json
from config import Config

from uploader.Metadata import ARCHIVEMATICA_METADATA_FILENAME


def create_metadata(form: dict, permissions: dict) -> None:
    """create archivematica metadata file"""

    if not Config.DEBUG:
        server = Config.DATAVERSE_SERVER
    else:
        server = Config.DATAVERSE_DEMO_SERVER

    if form is None | permissions is None:
        raise TypeError(
            "Expected form and permissions to be set,\ngot form: %s \n\npermissions: %s"
            % (form, permissions)
        )
    root: str = "objects/"
    metadata_list = [
        {
            "filename": root + filename,
            "dc.accesRights": permissions[filename],
        }
        for filename in permissions.keys()
    ]
    root_metadata = {
        "filename": root,
        "dc.title": form["title"],
        "dc.creator": form["author"],
        "dc.description": form["description"],
        "dc.subject": form["keywords"].append(form["subject"]),
        "dc.publisher": server + form["division"],
        "dc.dateSubmitted": form["dateOfDeposit"],
        "dc.language": "English",
        "dc.temporal": form["daterangeStart"],
        "other.researchProjectEndDate": form["researchEndDate"],
        "dc.coverage": "start={}, end={}".format(
            form["researchEndDate"], form["retention"]
        ),
        "dc.rights": form["license"],
        "dc.type": form["kindOfData"],
        "dc.isReferencedBy": form["publication"],
        "other.researchType": form["researchType"],
        "other.depositor": form["depositor"],
        "other.contributor": form["contributor"],
    }

    metadata_list.append(root_metadata)
    with open(ARCHIVEMATICA_METADATA_FILENAME, "w") as f:
        json.dump(metadata_list, f, indent=4)
    return None
