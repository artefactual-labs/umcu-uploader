# -*- coding: utf-8 -*-

import uuid

from config import CONFIGS
from flask import Flask, session

from uploader.navbar import NavBar


def create_app(config_name="default"):
    """Flask app factory, returns app instance."""
    app = Flask(__name__)
    app.config.from_object(CONFIGS[config_name])

    with app.app_context():
        from uploader.Transfer.views import transfer
        from uploader.Navigator.views import navigator
        from uploader.Upload.views import upload
        from uploader.Dataverse.views import dataverse
        from uploader.Metadata.views import metadata
        from uploader.Job.views import job

        app.register_blueprint(transfer)
        app.register_blueprint(navigator, url_prefix="/files")
        app.register_blueprint(metadata, url_prefix="/metadata")
        app.register_blueprint(upload, url_prefix="/upload")
        app.register_blueprint(dataverse, url_prefix="/dataverse")
        app.register_blueprint(job, url_prefix="/job")

        # Define navigation bar
        navbar = NavBar()
        navbar.add("Upload Research Data", "transfer.index")
        navbar.add("Metadata", "metadata.index")
        navbar.add("Access Rights", "navigator.index")
        navbar.add("Archivematica", "upload.index")
        navbar.add("Dataverse", "dataverse.index")
        navbar.add("Jobs", "job.index")

        # Initialize session ID, if need be
        @app.before_request
        def init_session_id():
            if not "session_id" in session:
                session["session_id"] = str(uuid.uuid4())

        # Inject navigation bar into templates
        @app.context_processor
        def inject_navbar():
            return dict(navbar=navbar)

    return app
