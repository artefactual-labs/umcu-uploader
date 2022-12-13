# -*- coding: utf-8 -*-

import os
from flask import Blueprint, render_template, redirect, url_for, session, flash
import sqlite3

import uploader.job as job_class

job = Blueprint("job", __name__, template_folder="templates")


@job.route("/", methods=["GET"])
def index():
    context = {}

    jobs = job_class.Job()

    # Set job list to empty if no sqlite data yet exists
    try:
        context["jobs"] = jobs.list(session["session_id"], 10)
    except sqlite3.OperationalError:
        context["jobs"] = []

    return render_template("job.html", **context)


@job.route("/clear", methods=["POST"])
def clear():
    jobs = job_class.Job()

    jobs.clear(session["session_id"])

    flash("Jobs cleared.", "info")

    return redirect(url_for("job.index"))
