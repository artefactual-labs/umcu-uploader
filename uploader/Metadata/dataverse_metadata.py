import json
import os

from uploader.Metadata import DATAVERSE_METADATA_FILENAME
from uploader.Transfer import helpers


def parse_form_data(form_data_raw):
    [
        author_values_raw,
        contactName_values_raw,
        contributor_values_raw,
        publication_values_raw,
        contactEmail_values_raw,
        software_values_raw,
        keyword_values_raw,
    ] = form_data_raw
    author_values = [
        {
            "authorName": {
                "typeName": "authorName",
                "multiple": False,
                "typeClass": "primitive",
                "value": x,
            }
        }
        for x in author_values_raw
    ]
    keyword_values = [
        {
            "keywordValue": {
                "typeName": "keywordValue",
                "multiple": False,
                "typeClass": "primitive",
                "value": x,
            }
        }
        for x in keyword_values_raw
    ]
    publication_values = [
        {
            "publicationCitation": {
                "typeName": "publicationCitation",
                "multiple": False,
                "typeClass": "primitive",
                "value": x,
            }
        }
        for x in publication_values_raw
    ]
    contactName_values = [
        {
            "datasetContactName": {
                "typeName": "datasetContactName",
                "multiple": False,
                "typeClass": "primitive",
                "value": x,
            }
        }
        for x in contactName_values_raw
    ]
    contactEmail_values = [
        {
            "datasetContactEmail": {
                "typeName": "datasetContactEmail",
                "multiple": False,
                "typeClass": "primitive",
                "value": x,
            }
        }
        for x in contactEmail_values_raw
    ]
    contact_values = []
    for index, item in enumerate(contactName_values):
        contact = item
        contact.update(contactEmail_values[index])
        contact_values.append(contact)
    contributor_values = [
        {
            "contributorName": {
                "typeName": "contributorName",
                "multiple": False,
                "typeClass": "primitive",
                "value": x,
            }
        }
        for x in contributor_values_raw
    ]
    software_values = [
        {
            "softwareName": {
                "typeName": "softwareName",
                "multiple": False,
                "typeClass": "primitive",
                "value": software,
            }
        }
        for software in software_values_raw
    ]
    # return all values
    return (
        author_values,
        keyword_values,
        publication_values,
        contact_values,
        contributor_values,
        software_values,
    )


def dv_json(form_data):
    [
        subject_value,
        title_value,
        description_value,
        licence_value,
        licence_description,
        depositorName_value,
        date_of_deposit_value,
        date_start_value,
        date_end_value,
        data_type_values,
        author_values,
        contributor_values,
        publication_values,
        contact_values,
        software_values,
        keyword_values,
    ] = form_data
    dv_metadata = {
        "datasetVersion": {
            "licence": licence_value,
            "termsOfUse": licence_description,
            "metadataBlocks": {
                "citation": {
                    "displayName": "Citation Metadata",
                    "fields": [
                        {
                            "typeName": "publication",
                            "multiple": True,
                            "typeClass": "compound",
                            "value": publication_values,
                        },
                        {
                            "typeName": "author",
                            "typeClass": "compound",
                            "multiple": True,
                            "value": author_values,
                        },
                        {
                            "typeName": "keyword",
                            "typeClass": "compound",
                            "multiple": True,
                            "value": keyword_values,
                        },
                        {
                            "typeName": "subject",
                            "typeClass": "controlledVocabulary",
                            "multiple": True,
                            "value": subject_value,
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
                            "value": title_value,
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
                                        "value": description_value,
                                    },
                                }
                            ],
                        },
                        {
                            "typeName": "contributor",
                            "typeClass": "compound",
                            "multiple": True,
                            "value": contributor_values,
                        },
                        {
                            "typeName": "datasetContact",
                            "multiple": True,
                            "typeClass": "compound",
                            "value": contact_values,
                        },
                        {
                            "typeName": "software",
                            "multiple": True,
                            "typeClass": "compound",
                            "value": software_values,
                        },
                        {
                            "typeName": "dateOfDeposit",
                            "typeClass": "primitive",
                            "multiple": False,
                            "value": date_of_deposit_value,
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
                                        "value": date_start_value,
                                    },
                                    "timePeriodCoveredEnd": {
                                        "typeName": "timePeriodCoveredEnd",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": date_end_value,
                                    },
                                },
                            ],
                        },
                        {
                            "typeName": "kindOfData",
                            "multiple": True,
                            "typeClass": "primitive",
                            "value": data_type_values,
                        },
                        {
                            "typeName": "depositor",
                            "multiple": False,
                            "typeClass": "primitive",
                            "value": depositorName_value,
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
