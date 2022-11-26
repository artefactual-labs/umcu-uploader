# -*- coding: utf-8 -*-

import hashlib
import json
import os
import tempfile

from flask import (
    Blueprint,
    redirect,
    abort,
    render_template,
    session,
    send_file,
    request,
    flash,
    current_app,
    url_for,
)
import magic

from uploader.Metadata import DATAVERSE_METADATA_FILENAME
from uploader.Metadata import arc_metadata
from uploader.Transfer import helpers

perms = {}

navigator = Blueprint("navigator", __name__, template_folder="templates")


@navigator.route("/", defaults={"req_path": ""}, methods=["GET", "POST"])
@navigator.route("/<path:req_path>", methods=["GET", "POST"])
def index(req_path):
    transfer_dir = helpers.get_transfer_directory()

    # Joining the transfer directory and the requested path
    abs_path = os.path.join(transfer_dir, req_path)

    # Return 404 if path doesn't exist or path is a file
    if not os.path.exists(abs_path) or os.path.isfile(abs_path):
        return abort(404)

    # Assemble back link path
    back_path = ""
    if req_path != "":
        back_path = "/files/" + "/".join(req_path.split("/")[0:-1])
        back_path = back_path.rstrip("/")

    # Get directory contents (expanded or per-directory)
    if request.args.get("expand") is not None:
        # Expanded view shouldn't take place in a transfer subdirectory
        if req_path:
            return redirect(url_for("navigator.index", expand=1))

        files = helpers.get_all_filepaths_in_directory(abs_path)
    else:
        files = os.listdir(abs_path)

    # Update permissions data, if sent
    if request.method == "POST":
        for file in files:
            entry_path = os.path.join(abs_path, file)
            form_field_name = (
                "perm_" + hashlib.md5(entry_path.encode("utf-8")).hexdigest()
            )

            if form_field_name in request.form:
                permission = request.form[form_field_name]

                perms[entry_path] = permission

        flash("Updated.", "primary")
        redirect(request.path)

    # Assemble directory data
    entries = []
    for file in files:
        entry_path = os.path.join(abs_path, file)

        entry = {
            "name": file,
            "size": os.path.getsize(entry_path),
            "is_dir": os.path.isdir(entry_path),
            "settable": True,
            "path_md5": hashlib.md5(entry_path.encode("utf-8")).hexdigest(),
        }

        # Apply rules for preventing permission setting
        if req_path == "" and (
            file == DATAVERSE_METADATA_FILENAME | file == arc.metadata.METADATA_FILENAME
        ):
            entry["settable"] = False

        if os.path.isdir(entry_path):
            entry["settable"] = False

        if not entry["is_dir"]:
            entry["mimetype"] = magic.from_file(entry_path, mime=True)

        if perms[entry_path] is not None:
            entry["permission"] = perms[entry_path]

        entries.append(entry)

    return render_template(
        "files.html", entries=entries, req_path=req_path, back_path=back_path
    )


@navigator.route("/preview", methods=["GET"])
def preview():
    JSON_tempfile = tempfile.NamedTemporaryFile()
    with open(JSON_tempfile.name, "w") as f:
        json.dump(perms, f, indent=4)
    # Trigger JSON download
    return send_file(
        JSON_tempfile.name,
        as_attachment=True,
        mimetype="application/json",
        download_name="metadata.json",
    )
