import json
import os

from uploader.Metadata import DATAVERSE_METADATA_FILENAME
from uploader.Transfer import helpers

def create_values (values, template):
    "takes a list of values and a template and creates a list of dicts"
    dv_value = [template[k].update({"value": v}) for (k, v) in values.items()]
    return dv_value


def parse_form_data(f):
    author_values = create_values(f.author, {
            "authorName": {
                "typeName": "authorName",
                "multiple": False,
                "typeClass": "primitive",
                "value": "",
            }
        })
    contactName_values = create_values(f.contactName, {
            "datasetContactName": {
                "typeName": "datasetContactName",
                "multiple": False,
                "typeClass": "primitive",
                "value": "",
            }
        })
    contributor_values = create_values(f.contributor, {
            "contributorName": {
                "typeName": "contributorName",
                "multiple": False,
                "typeClass": "primitive",
                "value": "",
            }
        })
    publication_values = create_values(f.publication,  {
            "publicationCitation": {
                "typeName": "publicationCitation",
                "multiple": False,
                "typeClass": "primitive",
                "value": "",
            }
        })
    contactEmail_values = create_values(f.contactEmail,  {
            "datasetContactEmail": {
                "typeName": "datasetContactEmail",
                "multiple": False,
                "typeClass": "primitive",
                "value": "",
            }
        })
    software_values = create_values(f.software,  {
            "softwareName": {
                "typeName": "softwareName",
                "multiple": False,
                "typeClass": "primitive",
                "value": "",
            }
        })
    keyword_values = create_values(f.keyword, {
            "keywordValue": {
                "typeName": "keywordValue",
                "multiple": False,
                "typeClass": "primitive",
                "value": "",
            }
        })
 
    contact_values = []
    for index, item in enumerate(contactName_values):
        contact = item
        contact.update(contactEmail_values[index])
        contact_values.append(contact)
    # return all values
    return [
        author_values,
        keyword_values,
        publication_values,
        contact_values,
        contributor_values,
        software_values,
    ]
    


def dv_json(f):
    dv_metadata = {
        "datasetVersion": {
            "licence": f.licence_value,
            "termsOfUse": f.licence_description,
            "metadataBlocks": {
                "citation": {
                    "displayName": "Citation Metadata",
                    "fields": [
                        {
                            "typeName": "publication",
                            "multiple": True,
                            "typeClass": "compound",
                            "value": f.publication_values,
                        },
                        {
                            "typeName": "author",
                            "typeClass": "compound",
                            "multiple": True,
                            "value": f.author_values,
                        },
                        {
                            "typeName": "keyword",
                            "typeClass": "compound",
                            "multiple": True,
                            "value": f.keyword_values,
                        },
                        {
                            "typeName": "subject",
                            "typeClass": "controlledVocabulary",
                            "multiple": True,
                            "value": f.subject_value,
                        },
                        {
                            "typeName": "language",
                            "typeClass": "controlledVocabulary",
                            "multiple": True,
                            "value": ["English"],
                        },
                        {
                            "typeName": "title",
                            "multiple": False,
                            "typeClass": "primitive",
                            "value": f.title_value,
                        },
                        {
                            "typeName": "dsDescription",
                            "typeClass": "compound",
                            "multiple": True,
                            "value": [
                                {
                                    "dsDescriptionValue": {
                                        "typeName": "dsDescriptionValue",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": f.description_value,
                                    },
                                }
                            ],
                        },
                        {
                            "typeName": "contributor",
                            "typeClass": "compound",
                            "multiple": True,
                            "value": f.contributor_values,
                        },
                        {
                            "typeName": "datasetContact",
                            "multiple": True,
                            "typeClass": "compound",
                            "value": f.contact_values,
                        },
                        {
                            "typeName": "software",
                            "multiple": True,
                            "typeClass": "compound",
                            "value": f.software_values,
                        },
                        {
                            "typeName": "dateOfDeposit",
                            "typeClass": "primitive",
                            "multiple": False,
                            "value": f.date_of_deposit_value,
                        },
                        {
                            "typeName": "timePeriodCovered",
                            "typeClass": "compound",
                            "multiple": True,
                            "value": [
                                {
                                    "timePeriodCoveredStart": {
                                        "typeName": "timePeriodCoveredStart",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": f.date_start_value,
                                    },
                                    "timePeriodCoveredEnd": {
                                        "typeName": "timePeriodCoveredEnd",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": f.date_end_value,
                                    },
                                },
                            ],
                        },
                        {
                            "typeName": "kindOfData",
                            "multiple": True,
                            "typeClass": "primitive",
                            "value": f.data_type_values,
                        },
                        {
                            "typeName": "depositor",
                            "multiple": False,
                            "typeClass": "primitive",
                            "value": f.depositorName_value,
                        },
                    ],
                },
            },
        },
    }
    filepath = os.path.join(
        helpers.get_transfer_directory(), DATAVERSE_METADATA_FILENAME
    )
    with open(filepath, "w") as dv_metadata_file:
        json.dump(dv_metadata, dv_metadata_file, indent=4)
