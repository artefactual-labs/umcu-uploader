# -*- coding: utf-8 -*-

import os
from flask import Blueprint, render_template
from uploader.Transfer import helpers

metadata = Blueprint("metadata", __name__, template_folder="templates")

@metadata.route('/')
def index():
    metadata_dir = helpers.get_transfer_directory(True)
    return render_template('metadata.html', metadata_directory=metadata_dir)

@metadata.route('/metadata/metadata/', methods=["POST"])
def update():
# update the metada json file with the new form metadata collected from the user
    transfer = helpers.get_transfer_directory()
    return transfer
