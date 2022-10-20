# -*- coding: utf-8 -*-

import os
from flask import Blueprint, render_template, request, session, flash, redirect, url_for, current_app
from flask_api import status

from uploader.Transfer import helpers

transfer = Blueprint("transfer", __name__, template_folder="templates")

@transfer.route('/')
def index():
    transfer_dir = helpers.get_transfer_directory()
    transfer_preset = helpers.transfer_directory_set_in_config()
    transfer_file_count, transfer_total_file_size = helpers.directory_count_and_size(transfer_dir)

    return render_template('transfer.html', transfer_directory=transfer_dir, transfer_preset=transfer_preset, transfer_file_count=transfer_file_count, transfer_total_file_size=transfer_total_file_size)

@transfer.route('/transfer', methods=["POST"])
def update():
    transfer_dir = request.form["transfer_directory"]

    if transfer_dir:
        if not os.path.exists(transfer_dir):
            flash("Path does not exist.", "danger")
            return redirect(url_for('transfer.index'))
        elif os.path.isfile(transfer_dir):
            flash("Path is a file not a directory.", "danger")
            return redirect(url_for('transfer.index'))
        else:
            session["transfer_directory"] = request.form["transfer_directory"]
            session.modified = True

            flash("Updated.", "primary")
            return redirect(url_for('transfer.index'))

    return "Unsuitable form data submitted", status.HTTP_400_BAD_REQUEST
