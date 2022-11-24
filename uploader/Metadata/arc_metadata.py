import os
import json

from uploader.Metadata.views import FORM
def create_archivematica_metadata(permissions):
    """create archivematica metadata file"""
    server = "https://dataverse.nl/"
    if os.getenv("DEBUG") == 'True':
       server = "https://demo.dataverse.nl/"
    if FORM == '':
        # TODO: better error here.
        return "no bueno"
    root = 'test'
    metadata ={
            "filename": root,
            "dc.title": FORM.title,
            "dc.creator": FORM.author,
            "dc.description": FORM.description,
            "dc.subject": FORM.subject,
            "dc.publisher": server+FORM.division,
            "dc.dateSubmitted": FORM.date,
            "dc.language": "English",
            "dc.coverage": FORM.startDate +", "+ FORM.endDate,
            "dc.temporal": FORM.startDate-FORM.retention[0] +", "+ FORM.endDate-FORM.retention[1],
            "dc.rights": FORM.license,
            "dc.type": FORM.kindOfData,
            "dc.isReferencedBy": FORM.publicationCitation,
            "other.researchType": FORM.researchType,
            "other.depositor": FORM.depositor,
            "other.depositor": FORM.depositor,
        }
    permissions =[{
            "filename": file,
            "dc.accesRights": permissions[file],
        } for file in permissions.keys()]

    with open("arc_metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
    return metadata
