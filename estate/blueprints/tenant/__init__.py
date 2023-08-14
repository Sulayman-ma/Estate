from flask import Blueprint

tenant = Blueprint('tenant', __name__)

from . import views