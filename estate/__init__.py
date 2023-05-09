"""
Application factory

App instance, initialize extensions, register blueprints.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect



login_manager = LoginManager()
login_manager.login_view = 'admin.login'
db = SQLAlchemy()
csrf = CSRFProtect()


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    config_object.init_app()

    # extensions
    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # blueprints
    from .blueprints.main import main
    from .blueprints.admin import admin

    app.register_blueprint(admin)
    app.register_blueprint(main)

    return app