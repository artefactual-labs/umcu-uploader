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
        dv_parsed_formdata = dataverse_metadata.parse_form_data(
            [
                author_values_raw,
                contactName_values_raw,
                contributor_values_raw,
                publication_values_raw,
                contactEmail_values_raw,
                software_values_raw,
                keyword_values_raw,
            ]
        )

        dataverse_metadata.dv_json(
            [ depositorName_value,
        description_value,
        title_value,
        licence_value,
        licence_description, depositorName_value,
        date_of_deposit_value,
        date_start_value,
        date_end_value,
        data_type_values, *dv_parsed_formdata]
        )
        flash("Metadata saved.", "primary")
        return redirect(url_for("metadata.updated"))

    return render_rawlate("metadata.html")


@metadata.route("/updated", methods=["GET"])
def updated():
    # TODO: this is a raworary solution to show the user that the metadata has been saved
    # This will be replaced with a proper success page or alternative that allows the user to change the metadata
    return render_rawlate("done.html")
