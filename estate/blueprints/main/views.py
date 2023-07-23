from . import main
from ... import db
from .forms import (
    RegisterResident
)
from flask_login import (
    login_required,
    logout_user,
    login_user,
    current_user
)
from flask import (
    render_template, 
    redirect,
    url_for,
    flash,
    request
)
from ...models import (
    User,
    Role,
    Payment,
    Flat,
    FlatType
)
from datetime import datetime, timedelta



@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/profile')
# @role_required('TENANT')
def profile():
    return render_template('main/profile.html')


# @main.route('/flats')
# def flats():
#     types = FlatType.query.all()
#     return render_template('main/flats.html', types=types)


@main.route('/lease', methods=['GET', 'POST'])
def lease():
    # agreeing to terms and conditions
    if request.method == 'POST':
        return redirect(url_for('.register')) 
    return render_template('main/lease.html')


@main.route('/make_payment', methods=['GET', 'POST'])
def make_payment():
    flat_types = FlatType.query.all()
    if request.method == 'POST':
        flash('Payment successful.', 'success')
        return redirect(url_for('.profile'))
    return render_template('main/make_payment.html', flat_types=flat_types)


@main.route('/renew_payment', methods=['GET', 'POST'])
@login_required
def renew_payment():
    return 'Renew payment here'


@main.route('/register', methods=['GET', 'POST'])
def register():
    """Register user and make payment. Redirected from .lease view"""
    form = RegisterResident()
    if form.validate_on_submit():
        try:
            user = User(
                fullname = form.fullname.data,
                email = form.email.data,
                number = int(form.number.data),
                password = form.password.data,
                # resident role is ID 1, no conflicts here
                role = Role.query.get(1),
                # account is only deactivated a certain time after lease is terminated
                is_active = True
            )
            user.generate_user_tag()
            db.session.add(user)
            db.session.commit()
            # after registeration, log them in and redirect to make payment
            login_user(user)
            return redirect(url_for('.make_payment'))
        except ValueError:
            flash('⚠ Invalid input, check passwords and other data', 'error')
        except:
            flash('⚠ An error has occured, please try again or contact an admin.', 'error')
    return render_template('main/register.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))