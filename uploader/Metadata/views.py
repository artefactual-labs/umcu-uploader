# -*- coding: utf-8 -*-

import os
from flask import Blueprint, render_template, request, session

metadata = Blueprint("metadata", __name__, template_folder="templates")

@metadata.route('/')
def index():
    return render_template('index.html')
