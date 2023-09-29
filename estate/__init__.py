"""
Application factory

App instance, initialize extensions, register blueprints.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate



login_manager = LoginManager()
login_manager.login_view = 'auth.login'
# use in case of login with multiple blueprints
# login_manager.blueprint_login_views = {
#     'tenant': '/login',
#     'admin': '/admin/login'
# }
db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    config_object.init_app()

    # extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # blueprints
    from .blueprints.tenant import tenant
    from .blueprints.admin import admin
    from .blueprints.owner import owner
    from .blueprints.auth import auth

    app.register_blueprint(admin)
    app.register_blueprint(tenant)
    app.register_blueprint(owner)
    app.register_blueprint(auth)

    return app