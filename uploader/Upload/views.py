# -*- coding: utf-8 -*-

import os
from flask import Blueprint, render_template, request, session, flash, redirect, url_for, current_app
from flask_api import status

from uploader.Transfer import helpers

upload = Blueprint("upload", __name__, template_folder="templates")

@upload.route('/')
def index():
    transfer_dir = helpers.get_transfer_directory(True)
    transfer_preset = helpers.transfer_directory_set_in_config()
    transfer_file_count, transfer_total_file_size = helpers.directory_count_and_size(transfer_dir)

    return render_template('upload.html', transfer_directory=transfer_dir, transfer_preset=transfer_preset, transfer_file_count=transfer_file_count, transfer_total_file_size=transfer_total_file_size)
