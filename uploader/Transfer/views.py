# -*- coding: utf-8 -*-

import os

from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from flask_api import status
from werkzeug.utils import secure_filename

from uploader.Navigator import permissions
from uploader.Transfer import helpers

transfer = Blueprint("transfer", __name__, template_folder="templates")

@transfer.route('/')
def index():
    transfer_dir = helpers.get_transfer_directory()

    transfer_file_count, transfer_total_file_size = helpers.directory_count_and_size(
        transfer_dir
    )

    return render_template('transfer.html', transfer_directory=transfer_dir, transfer_file_count=transfer_file_count, transfer_total_file_size=transfer_total_file_size)

@transfer.route('/upload', methods=['POST'])
def upload():
    # Check if the post request has the file part
    if 'files' not in request.files:
        flash("No file part", "danger")
        return redirect(url_for('transfer.index'))

    # Abort if no file have been uploaded
    files = request.files.getlist("files")

    # Parse top-level dircetory from first file uploaded
    top_level_directory = os.path.split(files[0].filename)[0]

    # Create unique directory
    data_dir = helpers.get_data_directory()
    transfer_dir = helpers.potential_dir_name(os.path.join(data_dir, top_level_directory))
    os.mkdir(transfer_dir)

    # Cycle through file data, create necessary subdirectories, and save files
    filecount = 0
    for file in files:
        filename = secure_filename(file.filename)

        # An empty directory sent won't have a filename
        if filename == "":
            flash("No files were uploaded", "danger")
            return redirect(url_for('transfer.index'))

        # Create subdirectory (or subdirectories if need be) and set permissions
        rel_subdir = os.path.dirname(file.filename)[len(top_level_directory) + 1:]
        subdir = os.path.join(transfer_dir, rel_subdir)

        if not os.path.isdir(subdir):
            os.makedirs(subdir)

        # Assemble filepath to write to
        filename = secure_filename(os.path.basename(file.filename))
        filepath = os.path.join(subdir, filename)

        # Write to file and set permissions
        with open(filepath, 'wb') as f:
            f.write(file.read())

    # Set default permissions
    permission_file_path = os.path.join(transfer_dir, permissions.PERMISSION_METADATA_FILENAME)
    perms = permissions.FilePermissions(permission_file_path)

    for file in helpers.get_all_filepaths_in_directory(transfer_dir, False):
        entry_path = os.path.join(transfer_dir, file)
        perms[entry_path] = "private"

    # Change transfer directory
    session["transfer_directory"] = transfer_dir
    session.modified = True

    flash("Files have been uploaded", "primary")
    return redirect(url_for('transfer.index'))
