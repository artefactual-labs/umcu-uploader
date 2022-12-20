# -*- coding: utf-8 -*-

import json
import os

from flask import Blueprint, render_template, redirect, url_for, session, flash, abort
import sqlite3
import yaml

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

    return render_template("index.html", **context)


@job.route("/clear", methods=["POST"])
def clear():
    jobs = job_class.Job()

    jobs.clear(session["session_id"])

    flash("Jobs cleared.", "info")

    return redirect(url_for("job.index"))


@job.route("/<int:id>", methods=["GET"])
def detail(id):
    context = {}

    jobs = job_class.Job()

    # Get data for job (if job was created by user)
    job = jobs.get(id, session["session_id"])

    if job is None:
        abort(404, description="Job not found")

    context["job"] = job

    # Unserialize job parameters and format them as YAML for display
    context["params"] = yaml.dump(json.loads(job["params"]))

    return render_template("detail.html", **context)
