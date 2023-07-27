from flask_login import login_user
from estate import create_app
from config import Config
from estate import db
from estate.models import (
    User,
    Role,
    Payment,
    Flat,
    FlatType
)
from flask import (
    render_template, 
    request,
    redirect,
    url_for,
    flash
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
            # detect admin user tag
            if user_tag.startswith('a'):
                return redirect(url_for('admin.dash'))
            else:
                if next is None or not next.startswith('/'):
                    next = url_for('main.index')
                return redirect(next)
        flash('Incorrect user ID or password.', 'error')
    return render_template('login.html')


@app.shell_context_processor
def context_processor():
    return dict(db=db, Role=Role, Payment=Payment, User=User, FlatType=FlatType, Flat=Flat)