import os
import json

from uploader.Metadata.views import FORM
METADATA_FILEPATH = os.path.join(os.path.dirname('metadata'), "metadata.json")

def create_metadata(permissions):
    """create archivematica metadata file"""
    server = "https://dataverse.nl/"
    if os.getenv("DEBUG") == "True":
        server = "https://demo.dataverse.nl/"
    if FORM is None:
        # TODO: better error here.
        raise TypeError("Expected form to be set, got None")
    root: str = 'objects/'
    metadata = {
        "filename": root,
        "dc.title": FORM.title,
        "dc.creator": FORM.author,
        "dc.description": FORM.description,
        "dc.subject": FORM.subject,
        "dc.publisher": server + FORM.division,
        "dc.dateSubmitted": FORM.date,
        "dc.language": "English",
        "dc.coverage": FORM.startDate + ", " + FORM.endDate,
        "dc.temporal": FORM.startDate
        - FORM.retention[0]
        + ", "
        + FORM.endDate
        - FORM.retention[1],
        "dc.rights": FORM.license,
        "dc.type": FORM.kindOfData,
        "dc.isReferencedBy": FORM.publicationCitation,
        "other.researchType": FORM.researchType,
        "other.depositor": FORM.depositor,
        "other.depositor": FORM.depositor,
    }
    permissions = [
        {
            "filename":root + filename,
            "dc.accesRights": permissions[filename],
        }
        for filename in permissions.keys()
    ]

    with open("metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
    return None
