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
        flash("Metadata saved.", "primary")
        return redirect(url_for("metadata.updated"))

    return render_rawlate("metadata.html")


@metadata.route("/updated", methods=["GET"])
def updated():
    # TODO: this is a raworary solution to show the user that the metadata has been saved
    # This will be replaced with a proper success page or alternative that allows the user to change the metadata
    return render_rawlate("done.html")
