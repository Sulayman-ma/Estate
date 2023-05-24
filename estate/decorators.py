from functools import wraps
from flask import abort, redirect, url_for
from flask_login import current_user
from .models import Role



def role_required(role: Role):
    """Custom role required decorator for views that require them.
    :param role: The role object."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.role == role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """Admin required decorator. Takes advantage of the role_required decorator and passes the Admin role object."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('admin.login'))
            if not current_user.role.name == 'ADMIN':
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator(f)