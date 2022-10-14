# -*- coding: utf-8 -*-

from flask import Flask


def create_app(config_name="default"):
    """Flask app factory, returns app instance."""
    app = Flask(__name__)

    return app
