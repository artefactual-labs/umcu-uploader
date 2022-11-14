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


@upload.route("/", methods=["GET"])
def index():
    transfer_dir = helpers.get_transfer_directory()
    transfer_file_count, transfer_total_file_size = helpers.directory_count_and_size(
        transfer_dir
    )

    return render_template(
        "upload.html",
        transfer_directory=transfer_dir,
        transfer_file_count=transfer_file_count,
        transfer_total_file_size=transfer_total_file_size,
    )


@upload.route("/", methods=["POST"])
def send():
    transfer_dir = helpers.get_transfer_directory()
    transfer_source_dir = current_app.config["TRANSFER_SOURCE_DIRECTORY"]

    transfer_name = request.form["transfer_name"]

    # Perform copy asynchronously
    destination_dir = os.path.join(transfer_source_dir, transfer_name)

    u = job.CreateTransferJob()
    u.params({"source": transfer_dir, "destination": destination_dir})
    u.start()

    flash("Copy started.", "primary")
    return redirect(url_for("upload.index"))
