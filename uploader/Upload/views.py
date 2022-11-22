# -*- coding: utf-8 -*-

import os
from flask import (
    Blueprint,
    current_app,
    render_template,
    url_for,
    request,
    redirect,
    flash,
)
from flask_api import status

from uploader.Upload import job
from uploader.Transfer import helpers

upload = Blueprint("upload", __name__, template_folder="templates")


@upload.route("/", methods=["GET", "POST"])
def index():
    transfer_dir = helpers.get_transfer_directory()
    transfer_file_count, transfer_total_file_size = helpers.directory_count_and_size(
        transfer_dir
    )

    # Assemble department options
    department_options = []
    for department_id in current_app.config['DEPARTMENTS'].keys():
        department = current_app.config['DEPARTMENTS'][department_id]
        department_options.append({"id": department_id, "name": department["name"]})

    transfer_source_dir = current_app.config["TRANSFER_SOURCE_DIRECTORY"]

    # Handle form submission
    if request.method == 'POST':
        transfer_name = request.form["transfer_name"]
        department_id = request.form["department_id"]

        # Make sure necessary values have been provided
        validation_failed = False

        if transfer_name == "":
            flash("Please enter a transfer name.", "danger")
            validation_failed = True

        if not transfer_source_dir:
            if department_id == "":
                flash("Please select a department.", "danger")
                validation_failed = True

        if not validation_failed:
            # Perform copy asynchronously
            if not transfer_source_dir:
                transfer_source_dir = current_app.config['DEPARTMENTS'][department_id]['transfer_source_directory']

            destination_dir = os.path.join(transfer_source_dir, transfer_name)

            u = job.CreateTransferJob()
            u.params({"source": transfer_dir, "destination": destination_dir})
            u.start()

            flash("Copy started.", "primary")

    return render_template(
        "upload.html",
        transfer_directory=transfer_dir,
        transfer_file_count=transfer_file_count,
        transfer_total_file_size=transfer_total_file_size,
        department_options=department_options,
        transfer_source_dir=transfer_source_dir,
        request=request
    )
