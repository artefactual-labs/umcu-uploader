# -*- coding: utf-8 -*-
import json
import os
from flask import Blueprint, render_template, request, url_for, redirect, flash
from uploader.Transfer import helpers
from uploader.Metadata import DATAVERSE_METADATA_FILENAME

metadata = Blueprint("metadata", __name__, template_folder="templates")


@metadata.route("/", methods=["GET", "POST"], defaults={"req_path": ""})
def index(req_path):
    if request.method == "POST":
        form_data = request.form
        # convert form data to dataverse json api format
        # https://guides.dataverse.org/en/latest/_downloads/4e04c8120d51efab20e480c6427f139c/dataset-create-new-all-default-fields.json
        description_value = form_data["dsDescription"]
        title_value = form_data["title"]
        licence_value = form_data["licenceType"]
        author_values_temp = [y for x, y in form_data.items() if x.startswith("author")]
        author_values = [
            {
                "authorName": {
                    "typeName": "authorName",
                    "multiple": False,
                    "typeClass": "primitive",
                    "value": x,
                }
            }
            for x in author_values_temp
        ]
        subject_value = ["Medicine, Health and Life Sciences"]
        keyword_values_temp = [
            y for x, y in form_data.items() if x.startswith("keyword")
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
            for x in keyword_values_temp
        ]
        publication_values_temp = [
            y for x, y in form_data.items() if x.startswith("relatedPublication")
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
            for x in publication_values_temp
        ]
        contactName_values_temp = [
            y for x, y in form_data.items() if x.startswith("datasetContactName")
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
            for x in contactName_values_temp
        ]
        contactEmail_values_temp = [
            y for x, y in form_data.items() if x.startswith("datasetContactEmail")
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
            for x in contactEmail_values_temp
        ]
        contact_values = []
        for index, item in enumerate(contactName_values):
            contact = item
            contact.update(contactEmail_values[index])
            contact_values.append(contact)
        print("contact values",contact_values)
        contributor_values_temp = [
            y for x, y in form_data.items() if x.startswith("contributor")
        ]
        contributor_values = [
            {
                "contributorName": {
                    "typeName": "contributorName",
                    "multiple": False,
                    "typeClass": "primitive",
                    "value": x,
                }
            }
            for x in contributor_values_temp
        ]
        software_values_temp = [
            y for x, y in form_data.items() if x.startswith("software")
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
            for software in software_values_temp
        ]
        date_of_deposit_value = form_data.get("depositDate")
        date_start_value = form_data.get("dateRangeStart")
        date_end_value = form_data.get("dateRangeEnd")
        data_type_values = [y for x, y in form_data.items() if x.startswith("dataType")]
        depositorName_value = "test"
        licence_description_value = "null"
        dv_metadata = {
            "datasetVersion": {
                "licence": licence_value,
                "termsOfUse": licence_description_value,
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
                                "typeName": "title",
                                "multiple": False,
                                "typeClass": "primitive",
                                "value": title_value,
                            },
                            {
                                "typeName": "dsDescription",
                                "typeClass": "compound",
                                "multiple": True,
                                "value": [{
                                    "dsDescriptionValue": {
                                        "typeName": "dsDescriptionValue",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": description_value,
                                    },
                                }],
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

        flash("Metadata saved.", "primary")
        return redirect(url_for("metadata.updated"))

    return render_template("metadata.html")

@metadata.route("/updated", methods=["GET"])
def updated():
    return render_template("done.html")