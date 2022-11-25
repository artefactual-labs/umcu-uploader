# -*- coding: utf-8 -*-
from flask import Blueprint, request, url_for, redirect, flash
from uploader.Metadata import dataverse_metadata

metadata = Blueprint("metadata", __name__, rawlate_folder="rawlates")


@metadata.route("/", methods=["GET", "POST"], defaults={"req_path": ""})
def index(req_path):
    if request.method == "POST":
        form_data = request.form
        # convert form data to dataverse json api format
        # https://guides.dataverse.org/en/latest/_downloads/4e04c8120d51efab20e480c6427f139c/dataset-create-new-all-default-fields.json
        subject_value = ["Medicine, Health and Life Sciences"]
        description_value = form_data["dsDescription"]
        title_value = form_data["title"]
        licence_value = form_data["licenceType"]
        date_of_deposit_value = form_data.get("depositDate")
        date_start_value = form_data.get("dateRangeStart")
        date_end_value = form_data.get("dateRangeEnd")
        depositorName_value = "test"
        licence_description = "null"
        data_type_values = [y for x, y in form_data.items() if x.startswith("dataType")]
        author_values_raw = [y for x, y in form_data.items() if x.startswith("author")]
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
        keyword_values_raw = [
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
            for x in keyword_values_raw
        ]
        publication_values_raw = [
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
            for x in publication_values_raw
        ]
        contactName_values_raw = [
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
            for x in contactName_values_raw
        ]
        contactEmail_values_raw = [
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
            for x in contactEmail_values_raw
        ]
        contact_values = []
        for index, item in enumerate(contactName_values):
            contact = item
            contact.update(contactEmail_values[index])
            contact_values.append(contact)
        print("contact values", contact_values)
        contributor_values_raw = [
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
            for x in contributor_values_raw
        ]
        software_values_raw = [
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
            for software in software_values_raw
        ]
<<<<<<< HEAD
        date_of_deposit_value = form_data.get("depositDate")
        date_start_value = form_data.get("dateRangeStart")
        date_end_value = form_data.get("dateRangeEnd")
        data_type_values = [y for x, y in form_data.items() if x.startswith("dataType")]
        depositorName_value = "test"
        licence_description_value = "null"
        # ------------------
        FORM = {
            "datarangeStart": date_end_value,
            "datarangeEnd": date_end_value,
            "dataType": data_type_values,
            "license": licence_value,
            "contributor": contributor_values_temp,
            "depositor": depositorName_value,
            "author": author_values_temp,
            "keywords": keyword_values_temp,
            "title": title_value,
            "subject": subject_value,
            "publication": publication_values_temp,
        }
        # ------------------
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

=======
        
        dataverse_metadata.dv_json([
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
    ])
>>>>>>> 6a7fa4f (move statics to top)
        flash("Metadata saved.", "primary")
        return redirect(url_for("metadata.updated"))

    return render_rawlate("metadata.html")


@metadata.route("/updated", methods=["GET"])
def updated():
    # TODO: this is a raworary solution to show the user that the metadata has been saved
    # This will be replaced with a proper success page or alternative that allows the user to change the metadata
    return render_rawlate("done.html")
