from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views, errors

"""Authentication and Errors Blueprint

Handles all forms of authentication and some form actions for the users.
Also handles all app errors with unique templates.
"""