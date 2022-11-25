# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_rawlate, url_for, redirect, flash
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
        licence_description = "null"
        date_of_deposit_value = form_data.get("depositDate")
        date_start_value = form_data.get("dateRangeStart")
        date_end_value = form_data.get("dateRangeEnd")
        depositorName_value = "test"
        data_type_values = [y for x, y in form_data.items() if x.startswith("dataType")]
        author_values_raw = [y for x, y in form_data.items() if x.startswith("author")]
        contactName_values_raw = [
            y for x, y in form_data.items() if x.startswith("datasetContactName")
        ]
        contributor_values_raw = [
            y for x, y in form_data.items() if x.startswith("contributor")
        ]
        publication_values_raw = [
            y for x, y in form_data.items() if x.startswith("relatedPublication")
        ]
        contactEmail_values_raw = [
            y for x, y in form_data.items() if x.startswith("datasetContactEmail")
        ]
        software_values_raw = [
            y for x, y in form_data.items() if x.startswith("software")
        ]
        keyword_values_raw = [
            y for x, y in form_data.items() if x.startswith("keyword")
        ]

        # ------------------
        FORM = {
            "datarangeStart": date_start_value,
            "datarangeEnd": date_end_value,
            "dataType": data_type_values,
            "dateOfDeposit": date_of_deposit_value,
            "license": licence_value,
            "contributor": contributor_values_raw,
            "depositor": depositorName_value,
            "author": author_values_raw,
            "keywords": keyword_values_raw,
            "title": title_value,
            "subject": subject_value,
            "publication": publication_values_raw,
            "contactName": contactName_values_raw,
            "contactEmail": contactEmail_values_raw,
            "software": software_values_raw,
            "description": description_value,
        }
        # ------------------
        dv_parsed_formdata = dataverse_metadata.parse_form_data(FORM)
        [
            author_values,
            keyword_values,
            publication_values,
            contact_values,
            contributor_values,
            software_values,
        ] = dv_parsed_formdata
        dv_form = {
            "datarangeStart": date_start_value,
            "datarangeEnd": date_end_value,
            "dataType": data_type_values,
            "dateOfDeposit": date_of_deposit_value,
            "license": licence_value,
            "contributor": contributor_values,
            "depositor": depositorName_value,
            "author": author_values,
            "keywords": keyword_values,
            "title": title_value,
            "subject": subject_value,
            "publication": publication_values,
            "contact": contact_values,
            "software": software_values,
            "description": description_value,
            "licenceDescription": licence_description,
        }

        dataverse_metadata.dv_json(dv_form)

        # TODO: add error handling
        #
        flash("Metadata saved.", "primary")
        return redirect(url_for("metadata.updated"))

    return render_rawlate("metadata.html")


@metadata.route("/updated", methods=["GET"])
def updated():
    # TODO: this is a raworary solution to show the user that the metadata has been saved
    # This will be replaced with a proper success page or alternative that allows the user to change the metadata
    return render_rawlate("done.html")
