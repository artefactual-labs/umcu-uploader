import json
import os

from uploader.Metadata import DATAVERSE_METADATA_FILENAME
from uploader.Transfer import helpers


def create_values(values: list, template: dict) -> list:
    "takes a list of values and a template and creates a list of dicts"
    dv_value = [template[template.keys()[0]].update({"value": v}) for v in values]
    return dv_value


def parse_form_data(f: dict) -> list:
    author_values = create_values(
        f.author,
        {
            "authorName": {
                "typeName": "authorName",
                "multiple": False,
                "typeClass": "primitive",
                "value": "",
            }
        },
    )
    contactName_values = create_values(
        f.contactName,
        {
            "datasetContactName": {
                "typeName": "datasetContactName",
                "multiple": False,
                "typeClass": "primitive",
                "value": "",
            }
        },
    )
    contributor_values = create_values(
        f.contributor,
        {
            "contributorName": {
                "typeName": "contributorName",
                "multiple": False,
                "typeClass": "primitive",
                "value": "",
            }
        },
    )
    publication_values = create_values(
        f.publication,
        {
            "publicationCitation": {
                "typeName": "publicationCitation",
                "multiple": False,
                "typeClass": "primitive",
                "value": "",
            }
        },
    )
    contactEmail_values = create_values(
        f.contactEmail,
        {
            "datasetContactEmail": {
                "typeName": "datasetContactEmail",
                "multiple": False,
                "typeClass": "primitive",
                "value": "",
            }
        },
    )
    software_values = create_values(
        f.software,
        {
            "softwareName": {
                "typeName": "softwareName",
                "multiple": False,
                "typeClass": "primitive",
                "value": "",
            }
        },
    )
    keyword_values = create_values(
        f.keywords,
        {
            "keywordValue": {
                "typeName": "keywordValue",
                "multiple": False,
                "typeClass": "primitive",
                "value": "",
            }
        },
    )

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


def dv_json(f: dict) -> None:
    dv_metadata = {
        "datasetVersion": {
            "licence": f.licence,
            "termsOfUse": f.licence_description,
            "metadataBlocks": {
                "citation": {
                    "displayName": "Citation Metadata",
                    "fields": [
                        {
                            "typeName": "publication",
                            "multiple": True,
                            "typeClass": "compound",
                            "value": f.publications,
                        },
                        {
                            "typeName": "author",
                            "typeClass": "compound",
                            "multiple": True,
                            "value": f.authors,
                        },
                        {
                            "typeName": "keyword",
                            "typeClass": "compound",
                            "multiple": True,
                            "value": f.keywords,
                        },
                        {
                            "typeName": "subject",
                            "typeClass": "controlledVocabulary",
                            "multiple": True,
                            "value": f.subject,
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
                            "value": f.title,
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
                                        "value": f.description,
                                    },
                                }
                            ],
                        },
                        {
                            "typeName": "contributor",
                            "typeClass": "compound",
                            "multiple": True,
                            "value": f.contributors,
                        },
                        {
                            "typeName": "datasetContact",
                            "multiple": True,
                            "typeClass": "compound",
                            "value": f.contacts,
                        },
                        {
                            "typeName": "software",
                            "multiple": True,
                            "typeClass": "compound",
                            "value": f.software,
                        },
                        {
                            "typeName": "dateOfDeposit",
                            "typeClass": "primitive",
                            "multiple": False,
                            "value": f.date_of_deposit,
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
                                        "value": f.date_start,
                                    },
                                    "timePeriodCoveredEnd": {
                                        "typeName": "timePeriodCoveredEnd",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": f.date_end,
                                    },
                                },
                            ],
                        },
                        {
                            "typeName": "kindOfData",
                            "multiple": True,
                            "typeClass": "primitive",
                            "value": f.data_types,
                        },
                        {
                            "typeName": "depositor",
                            "multiple": False,
                            "typeClass": "primitive",
                            "value": f.depositorName,
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
