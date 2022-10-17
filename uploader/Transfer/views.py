# -*- coding: utf-8 -*-

import os
from flask import Blueprint, render_template, request, session

transfer = Blueprint("transfer", __name__, template_folder="templates")

@transfer.route('/', defaults={'req_path': ''})
@transfer.route('/<path:req_path>')
def index(req_path):
    transfer_dir = ""
    if "transfer_directory" in session:
        transfer_dir = session["transfer_directory"]

    return render_template('transfer.html', transfer_directory=transfer_dir)

@transfer.route('/transfer', methods=["POST"])
def update():
    if "transfer_directory" in request.form:
        transfer_dir = request.form["transfer_directory"]
        if not os.path.exists(transfer_dir):
            message = "Path does not exist."
        elif os.path.isfile(transfer_dir):
            message = "Path is a file not a directory."
        else:
            session["transfer_directory"] = request.form["transfer_directory"]
            message = "Updated."

    return render_template('transfer.html', message=message)
