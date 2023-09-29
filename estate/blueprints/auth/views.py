from . import auth
from .forms import EditProfile
from ... import db
from ...models import User
from ...decorators import role_required
from datetime import timedelta
from flask import (
    render_template,
    redirect,
    request,
    url_for,
    flash,
)
from flask_login import (
    login_required,
    login_user,
    logout_user,
    current_user
)
from sqlalchemy.exc import IntegrityError



@auth.route('/edit_profile/<int:id>', methods=['GET', 'POST', 'PUT'])
@login_required
def edit_profile(id):
    """The edit profile page for all users, both tenant and owners."""
    form = EditProfile(obj=current_user)
    if form.validate_on_submit():
        try:
            current_user.username = form.username.data
            current_user.first_name = form.first_name.data
            current_user.middle_name = form.middle_name.data or ''
            current_user.last_name = form.last_name.data
            current_user.number = form.number.data
            # if current_user.is_new:
            #     current_user.is_new = False
            # db.session.add(current_user._get_current_object())
            db.session.commit()
            flash('Edit successful ✔', 'success')
        # TODO: validation handler
        except IntegrityError:
            flash('⚠ Username already taken', 'misc')
            return redirect(url_for('.edit_profile', id=id))
        except:
            flash('⚠ An error has occured, please contact an admin if error persists.', 'error')
            return redirect(url_for('.edit_profile', id=id))
        # redirect to appropriate profile
        endpoint = '{}.index'.format(current_user.role.lower())
        return redirect(url_for(endpoint))
    if current_user.is_new:
        flash('ℹ Pleae complete your profile below', 'misc')
    return render_template('shared/edit_profile.html', form=form)


@auth.route('/', methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            # with remember me token for 1 hour
            login_user(user, duration=timedelta(hours=1))
            next = request.args.get('next')
            endpoint = '{}.index'.format(user.role.lower())
            # generate user blueprint endpoint with role name
            if next is None or not next.startswith('/'):
                next = url_for(endpoint)
            try:
                return redirect(next)
            except:
                pass
        flash('Incorrect user ID or password.', 'error')
    return render_template('shared/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))