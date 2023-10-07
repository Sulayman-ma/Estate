from . import auth
from flask_login import current_user
from flask import (
    redirect,
    url_for,
    flash,
    render_template
)



@auth.app_errorhandler(403)
def forbidden(e):
    """403 error handler.

    An anonymous user attempts to access a blueprint, upon being redirected to login, they are authenticated and if they are unauthorized, they are then redirected to their appropriate blueprint."""
    endpoint = '{}.index'.format(current_user.role.lower())
    flash('ACCESS DENIED', 'error')
    return redirect(url_for(endpoint))


@auth.app_errorhandler(404)
def not_found(e):
    return render_template('errors/404.html'), 404