# -*- coding: utf-8 -*-

import hashlib
import os
import tempfile 

from flask import Blueprint, redirect, abort, render_template, session, send_file, request, flash, current_app
import magic

from uploader.Navigator import permissions
from uploader.Transfer import helpers

navigator = Blueprint("navigator", __name__, template_folder="templates")

@navigator.route('/', defaults={'req_path': ''}, methods=["GET", "POST"])
@navigator.route('/<path:req_path>', methods=["GET", "POST"])
def index(req_path):
    transfer_dir = helpers.get_transfer_directory()

    # Joining the transfer directory and the requested path
    abs_path = os.path.join(transfer_dir, req_path)
    permission_file_path = os.path.join(transfer_dir, permissions.PERMISSION_METADATA_FILENAME)

    # Return 404 if path doesn't exist or path is a file
    if not os.path.exists(abs_path) or os.path.isfile(abs_path):
        return abort(404)

    # Assemble back link path
    back_path = ""
    if req_path != "":
        back_path = "/files/" + "/".join(req_path.split("/")[0:-1])
        back_path = back_path.rstrip("/")

    # Get directory contents
    files = os.listdir(abs_path)

    # Update permissions data, if sent
    if request.method == 'POST':
        for file in files:
            entry_path = os.path.join(abs_path, file)
            form_field_name = "perm_" + hashlib.md5(entry_path.encode('utf-8')).hexdigest()

            if form_field_name in request.form:
                permission = request.form[form_field_name]

                permissions.set_permission(permission_file_path, entry_path, permission)

        flash("Updated.", "primary")
        redirect(request.path)

    # Assemble directory data
    permission_data = permissions.read_permissions(permission_file_path)

    entries = []
    for file in files:
        entry_path = os.path.join(abs_path, file)

        entry = {
            "name": file,
            "size": os.path.getsize(entry_path),
            "is_dir": os.path.isdir(entry_path),
            "path_md5": hashlib.md5(entry_path.encode('utf-8')).hexdigest()
        }

        if not entry["is_dir"]:
            entry["mimetype"] = magic.from_file(entry_path, mime = True)

        if entry_path in permission_data:
            entry["permission"] = permission_data[entry_path]

        entries.append(entry)

    return render_template('files.html', entries=entries, req_path=req_path, back_path=back_path, permissions_filename=permissions.PERMISSION_METADATA_FILENAME)

@navigator.route('/preview', methods=["GET"])
def preview():
    transfer_dir = helpers.get_transfer_directory()
    csv_tempfile = tempfile.NamedTemporaryFile()

    permissions.write_permissions_to_csv(transfer_dir, csv_tempfile.name)

    return send_file(csv_tempfile.name, as_attachment=True, mimetype="text/csv", download_name="metadata.csv")
