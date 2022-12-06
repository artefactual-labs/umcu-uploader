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
    session
)
from flask_api import status

from uploader.Upload import job
from uploader.Transfer import helpers
from uploader.Metadata import views, form

upload = Blueprint("upload", __name__, template_folder="templates")


@upload.route("/", methods=["GET", "POST"])
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
        "request": request
    }

    # Set transfer name from session, if available
    if "transfer_name" in session:
        context["transfer_name"] = session["transfer_name"]

    # Assemble division options and add to template context
    division_options = []
    for division_id in current_app.config['DIVISIONS'].keys():
        division = current_app.config['DIVISIONS'][division_id]
        division_options.append({"id": division_id, "name": division["name"]})

    context["division_options"] = division_options

    context["transfer_source_dir"] = current_app.config["TRANSFER_SOURCE_DIRECTORY"]

    # Handle form submission
    if request.method == 'POST':
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
            context["transfer_source_dir"] = current_app.config['DIVISIONS'][division_id]['transfer_source_directory']

        if not os.path.isdir(context["transfer_source_dir"]):
            context["transfer_source_dir"] = None

            flash("Unable to copy to transfer source directory as it doesn't exist.", "danger")
        else:
            destination_dir = os.path.join(context["transfer_source_dir"], context["transfer_name"])

            f = form.FormData(views.FORM_FILEPATH)
            f.load()
            u = job.CreateTransferJob()
            u.params({"source": transfer_dir, "destination": destination_dir, "form": f.form,})
            u.start()

            flash("Copy to transfer source directory started.", "primary")

    return render_template(
        "upload.html",
        **context
    )
