# -*- coding: utf-8 -*-

from flask import Flask


def create_app(config_name="default"):
    """Flask app factory, returns app instance."""
    app = Flask(__name__)

    with app.app_context():

        from uploader.Navigator.views import navigator

        app.register_blueprint(navigator, url_prefix="/files")

    return app
