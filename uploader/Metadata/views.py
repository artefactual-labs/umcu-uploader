# -*- coding: utf-8 -*-
import os
from flask import Blueprint, request, render_template, url_for, redirect, flash
from uploader.Metadata import DIVISIONS_FILE_PATH, dataverse_metadata
from config import Config
from uploader.Metadata.form import FormData
from uploader.Metadata.helpers import get_division_acronym, get_raw_data, get_retention
from uploader.Transfer.helpers import get_transfer_directory

metadata = Blueprint("metadata", __name__, template_folder="templates")


@metadata.route("/", methods=["GET", "POST"], defaults={"req_path": ""})
def index(req_path: str):
    if request.method == "POST":
        form_data = request.form
        # convert form data to dataverse json api format
        # https://guides.dataverse.org/en/latest/_downloads/4e04c8120d51efab20e480c6427f139c/dataset-create-new-all-default-fields.json
        depositorName_value = Config.DEPOSITOR_NAME
        subject_value = ["Medicine, Health and Life Sciences"]
        description_value = form_data["dsDescription"]
        title_value = form_data["title"]
        licence_value = form_data["licenceType"]
        researchType_value = form_data["researchType"]
        licence_description = "This dataset is licensed. Please see the license for more information."

        date_of_deposit_value = form_data["depositDate"]
        date_start_value = form_data["dateRangeStart"]
        date_end_value = form_data["dateRangeEnd"]
        researchEndDate_value = form_data["researchEndDate"]

        data_type_values = get_raw_data(form_data, "dataType")
        author_values_raw = get_raw_data(form_data, "author")
        contactName_values_raw = get_raw_data(form_data, "datasetContactName")
        contributor_values_raw = get_raw_data(form_data, "contributor")
        publication_values_raw = get_raw_data(form_data, "relatedPublication")
        contactEmail_values_raw = get_raw_data(form_data, "datasetContactEmail")
        software_values_raw = get_raw_data(form_data, "software")
        keyword_values_raw = get_raw_data(form_data, "keyword")

        retention_value = get_retention(
            researchEndDate_value, researchType_value
        )
        # ------------------
        form = {
            "retention": retention_value,
            "researchType": researchType_value,
            "daterangeStart": date_start_value,
            "daterangeEnd": date_end_value,
            "researchEndDate": researchEndDate_value,
            "kindOfData": data_type_values,
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
            'divisionAcronym': get_division_acronym(DIVISIONS_FILE_PATH, form_data['umcuDivision']),
        }

        transfer_dir = get_transfer_directory()
        FORM_FILEPATH = os.path.join(transfer_dir, 'raw_form.json')
        metadataform = FormData(FORM_FILEPATH)
        # save this
        metadataform.save(form)
        # ------------------
        dv_parsed_formdata = dataverse_metadata.parse_form_data(form)
        [
            author_values,
            keyword_values,
            publication_values,
            contact_values,
            contributor_values,
            software_values,
        ] = dv_parsed_formdata
        dv_form = {
            "daterangeStart": date_start_value,
            "daterangeEnd": date_end_value,
            "dataTypes": data_type_values,
            "dateOfDeposit": date_of_deposit_value,
            "licence": licence_value,
            "contributors": contributor_values,
            "depositor": depositorName_value,
            "authors": author_values,
            "keywords": keyword_values,
            "title": title_value,
            "subject": subject_value,
            "software": software_values,
            "publications": publication_values,
            "contacts": contact_values,
            "description": description_value,
            "licenceDescription": licence_description,
        }

        dataverse_metadata.dv_json(dv_form)

        flash("Metadata saved.", "primary")
        return redirect(url_for("metadata.updated"))

    return render_template("metadata.html")


@metadata.route("/updated", methods=["GET"])
def updated() -> str:
    # This will be replaced with a proper success page or alternative that allows the user to change the metadata
    return render_template("done.html")
