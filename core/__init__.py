from .main import app as application
from flask import redirect, url_for

import os

import dotenv

dotenv.load_dotenv(".env")


@application.route("/")
def home():
    """Redirect users to default endpoint"""
    return redirect(url_for("v1"))
