# -*- coding: utf-8 -*-

import os
from flask import Blueprint, render_template, request, session
from uploader.Transfer import helpers

metadata = Blueprint("metadata", __name__, template_folder="templates")

@metadata.route('/', defaults={'req_path': ''})
def index(req_path):
    metadata_dir = ""
    if "metadata_directory" in session:
        metadata_dir = session["metadata_directory"]

    return render_template('metadata.html', metadata_directory=metadata_dir)

@metadata.route('/metadata/metadata/', methods=["POST"])
def update():
# update the metada json file with the new form metadata collected from the user
    transfer = helpers.get_transfer_directory()
    return transfer
