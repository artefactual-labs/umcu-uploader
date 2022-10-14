# -*- coding: utf-8 -*-

import os
from flask import Blueprint, redirect, url_for, abort, render_template, send_file

BASE_DIR = '/tmp'

navigator = Blueprint("navigator", __name__, template_folder="templates")

#@navigator.route("/files", methods=["GET"])
@navigator.route('/', defaults={'req_path': ''})
@navigator.route('/<path:req_path>')
def index(req_path):
    """Define handling for application's / route."""
    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Assemble back link path
    back_path = ""
    if req_path != "":
        back_path = "/files/" + "/".join(req_path.split("/")[0:-1])
        back_path = back_path.rstrip("/")

    # Show directory contents
    files = os.listdir(abs_path)

    entries = []
    for file in files:
        entry_path = os.path.join(abs_path, file)

        entries.append({
            "name": file,
            "size": os.path.getsize(entry_path)
        })

    return render_template('files.html', entries=entries, back_path=back_path)
