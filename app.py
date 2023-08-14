from flask_login import login_user
from estate import create_app, db
from config import Config
from estate.models import (
    User,
    Payment,
    Flat,
    flat_link
)
from flask import (
    render_template, 
    request,
    redirect,
    url_for,
    flash,
    abort
)
from datetime import timedelta



app = create_app(Config)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """The login view is here in an attempt to use it for all users and redirect to the appropriate blueprint."""
    if request.method == 'POST':
        user_tag = request.form.get('user_tag')
        password = request.form.get('password')
        user = User.query.filter_by(user_tag=user_tag).first()
        if user is not None and user.check_password(password):
            login_user(user, remember=True, duration=timedelta(hours=1))
            next = request.args.get('next')
            # generate user blueprint endpoint with role
            endpoint = '{}.index'.format(user.role.lower())
            # send user to requested page if they are authorized
            if user.role.lower() in next:
                return redirect(next)
            # abort otherwise
            if user.role.lower() not in next:
                return abort(403)
            # otherwise send user to homepage of their appropriate blueprint
            if next is None or not next.startswith('/'):
                next = url_for(endpoint)
            return redirect(next)
        flash('Incorrect user ID or password.', 'error')
    return render_template('login.html')


@app.shell_context_processor
def context_processor():
    return dict(db=db, Payment=Payment, User=User, Flat=Flat, flat_link=flat_link)