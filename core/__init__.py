from .main import app as application
from flask import redirect, url_for

import os

import dotenv

dotenv.load_dotenv(os.path.join(os.environ.get("ENV_DIR", os.getcwd()), ".env"))


@application.route("/")
def home():
    """Redirect users to default endpoint"""
    return redirect(url_for("v1"))
