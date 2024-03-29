# -*- coding: utf-8 -*-

import os
from flask import (
    Blueprint,
    current_app,
    render_template,
    url_for,
    request,
    flash,
    session,
)
from flask_api import status

from uploader.Archivematica import jobs
from uploader.Transfer import helpers
from uploader.Metadata import FORM_FILE_NAME, form

archivematica = Blueprint("archivematica", __name__, template_folder="templates")


@archivematica.route("/", methods=["GET", "POST"])
def index():
    # Initialize template context
    transfer_dir = helpers.get_transfer_directory()
    transfer_file_count, transfer_total_file_size = helpers.directory_count_and_size(
        transfer_dir
    )

    context = {
        "transfer_directory": transfer_dir,
        "transfer_file_count": transfer_file_count,
        "transfer_total_file_size": transfer_total_file_size,
        "request": request,
    }

    # Set transfer name from session, if available
    if "transfer_name" in session:
        context["transfer_name"] = session["transfer_name"]

    # Warn user if Dataverse metadata hasn't been set for current transfer
    form_filepath = os.path.join(transfer_dir, FORM_FILE_NAME)

    f = form.FormData(form_filepath)
    f.load()

    if f.form is None:
        flash(
            "Please specify metadata before exporting transfer to Archivematica.",
            "danger",
        )

    # Assemble division options and add to template context
    division_options = []
    for division_id in current_app.config["DIVISIONS"].keys():
        division = current_app.config["DIVISIONS"][division_id]
        division_options.append({"id": division_id, "name": division["name"]})

    context["division_options"] = division_options

    context["transfer_source_dir"] = current_app.config["TRANSFER_SOURCE_DIRECTORY"]

    # Handle form submission
    if request.method == "POST":
        context["transfer_name"] = request.form["transfer_name"]

        # Get division ID from form data, if available
        division_id = ""
        if "division_id" in request.form:
            division_id = request.form["division_id"]

        # Make sure necessary values have been provided
        if context["transfer_name"] == "":
            flash("Please enter a transfer name.", "danger")
            return render_template("upload.html", **context)

        if not context["transfer_source_dir"] and division_id == "":
            flash("Please select a division.", "danger")
            return render_template("upload.html", **context)

        # Perform copy, asynchronously, to transfer source directory
        if not context["transfer_source_dir"]:
            context["transfer_source_dir"] = current_app.config["DIVISIONS"][
                division_id
            ]["transfer_source_directory"]

        if not os.path.isdir(context["transfer_source_dir"]):
            context["transfer_source_dir"] = None

            flash(
                "Unable to copy to transfer source directory as it doesn't exist.",
                "danger",
            )
        else:
            destination_dir = os.path.join(
                context["transfer_source_dir"], context["transfer_name"]
            )

            job = jobs.CopyTransferJob()

            job.user_id = session["session_id"]
            job.source = transfer_dir
            job.destination = destination_dir
            job.form = f.form

            job.do()

            flash("Copy to transfer source directory started.", "primary")

    return render_template("upload.html", **context)
