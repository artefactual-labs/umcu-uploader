# -*- coding: utf-8 -*-

from config import CONFIGS
from flask import Flask


def create_app(config_name="default"):
    """Flask app factory, returns app instance."""
    app = Flask(__name__)
    app.config.from_object(CONFIGS[config_name])

    with app.app_context():

        from uploader.Transfer.views import transfer
        from uploader.Navigator.views import navigator
        from uploader.Metadata.views import metadata

        app.register_blueprint(transfer)
        app.register_blueprint(navigator, url_prefix="/files")
        app.register_blueprint(metadata, url_prefix="/metadata")

    return app
