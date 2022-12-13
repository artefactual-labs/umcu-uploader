# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash, current_app, session

from uploader.configutil import config_subset_dict
from uploader.Dataverse import jobs

dataverse = Blueprint("dataverse", __name__, template_folder="templates")


@dataverse.route("/", methods=["GET", "POST"])
def index():
    context = {}

    # Handle form submission
    if request.method == "POST":
        if "uuid" in request.form:
            uuid = request.form["uuid"]

            u = jobs.CreateDataverseDatasetFromAipJob()

            # Create subject of configuration because some config variables
            # aren't JSON serializable
            config = config_subset_dict(
                current_app.config,
                [
                    "STORAGE_SERVER_URL",
                    "STORAGE_SERVER_USER",
                    "STORAGE_SERVER_API_KEY",
                    "STORAGE_SERVER_BASIC_AUTH_USER",
                    "STORAGE_SERVER_BASIC_AUTH_PASSWORD",
                    "DATAVERSE_SERVER",
                    "DATAVERSE_DEMO_SERVER",
                    "DEMO_MODE",
                    "DATAVERSE_API_KEY",
                ],
            )

            u.params({"user_id": session["session_id"], "uuid": uuid, "config": config})
            u.start()

            flash("Started downloading AIP and importing into Dataverse", "info")

    return render_template("dataverse.html", **context)
