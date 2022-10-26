# -*- coding: utf-8 -*-

from config import CONFIGS
from flask import Flask

from uploader.navbar import NavBar


def create_app(config_name="default"):
    """Flask app factory, returns app instance."""
    app = Flask(__name__)
    app.config.from_object(CONFIGS[config_name])

    with app.app_context():
        from uploader.Transfer.views import transfer
        from uploader.Navigator.views import navigator
        from uploader.Upload.views import upload

        app.register_blueprint(transfer)
        app.register_blueprint(navigator, url_prefix="/files")
        app.register_blueprint(upload, url_prefix="/upload")

        # Define navigation bar
        navbar = NavBar()
        navbar.add("Select Research Data", "transfer.index")
        navbar.add("File Permissions", "navigator.index")
        navbar.add("Upload", "upload.index")

        # Inject navigation bar into templates
        @app.context_processor
        def inject_navbar():
            return dict(navbar=navbar)

    return app
