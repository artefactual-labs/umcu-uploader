import os
import json
from config import Config

METADATA_FILENAME = "metadata.json"


def create_metadata(form: dict, permissions: dict) -> None:
    """create archivematica metadata file"""

    if form is None | permissions is None:
        raise TypeError(
            "Expected form and permissions to be set,\ngot form: %s \n\npermissions: %s"
            % (form, permissions)
        )
    root: str = "objects/"
    metadata = {
        "filename": root,
        "dc.title": form["title"],
        "dc.creator": form["author"],
        "dc.description": form["description"],
        "dc.subject": form["keywords"].append(form["subject"]),
        "dc.publisher": Config.SERVER + form["division"],
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
    permissions = [
        {
            "filename": root + filename,
            "dc.accesRights": permissions[filename],
        }
        for filename in permissions.keys()
    ]

    with open(METADATA_FILENAME, "w") as f:
        json.dump(metadata, f, indent=4)
    return None
