# -*- coding: utf-8 -*-

import os
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from flask_api import status
from werkzeug.utils import secure_filename

from uploader.Transfer import helpers

transfer = Blueprint("transfer", __name__, template_folder="templates")

@transfer.route('/')
def index():
    transfer_dir = helpers.get_transfer_directory(True)
    transfer_preset = helpers.transfer_directory_set_in_config()

    return render_template('transfer.html', transfer_directory=transfer_dir, transfer_preset=transfer_preset)

@transfer.route('/research', methods=["POST"])
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

UPLOAD_FOLDER = '/tmp/upload'
#ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@transfer.route('/upload', methods=['POST'])
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('transfer.index'))
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('transfer.index'))
    if file:
        filename = secure_filename(file.filename)
        with open(os.path.join(UPLOAD_FOLDER, filename), 'w') as f:
            flash('file has been uploaded')
            return redirect(url_for('transfer.index'))
