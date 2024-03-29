from functools import wraps
from flask import abort, current_app
from flask_login import current_user



def role_required(role):
    """Custom role required decorator for views.
    :param role: The role of the user."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # redirect unauthenticated users
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            if current_user.role != role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator