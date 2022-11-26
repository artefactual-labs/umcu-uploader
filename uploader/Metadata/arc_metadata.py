import os
import json

METADATA_FILEPATH = os.path.join(os.path.dirname("metadata"), "metadata.json")


def create_metadata(form, permissions):
    """create archivematica metadata file"""
    server = "https://dataverse.nl/"
    if os.getenv("DEBUG") == "True":
        server = "https://demo.dataverse.nl/"
    if form is None:
        # TODO: better error here.
        raise TypeError("Expected form to be set, got None")
    root: str = "objects/"
    metadata = {
        "filename": root,
        "dc.title": form.title,
        "dc.creator": form.author,
        "dc.description": form.description,
        "dc.subject": form.subject,
        "dc.publisher": server + form.division,
        "dc.dateSubmitted": form.date,
        "dc.language": "English",
        "dc.coverage": form.startDate + ", " + form.endDate,
        "dc.temporal": form.startDate
        - form.retention[0]
        + ", "
        + form.endDate
        - form.retention[1],
        "dc.rights": form.license,
        "dc.type": form.kindOfData,
        "dc.isReferencedBy": form.publicationCitation,
        "other.researchType": form.researchType,
        "other.depositor": form.depositor,
        "other.depositor": form.depositor,
    }
    permissions = [
        {
            "filename": root + filename,
            "dc.accesRights": permissions[filename],
        }
        for filename in permissions.keys()
    ]

    with open("metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
    return None
