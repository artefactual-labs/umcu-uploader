import json
import os

from uploader.Metadata import DATAVERSE_METADATA_FILENAME
from uploader.Transfer import helpers


def dv_json(form_data):
    [
        depositorName_value,
        description_value,
        title_value,
        licence_value,
        licence_description,
        author_values,
        subject_value,
        keyword_values,
        publication_values,
        contact_values,
        contributor_values,
        software_values,
        date_of_deposit_value,
        date_start_value,
        date_end_value,
        data_type_values,
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
