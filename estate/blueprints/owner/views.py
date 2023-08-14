from . import owner
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
    Payment,
    Flat
)
from datetime import datetime, timedelta



@owner.route('/profile')
# @role_required('TENANT')
def profile():
    return render_template('owner/profile.html')


# @owner.route('/flats')
# def flats():
#     types = FlatType.query.all()
#     return render_template('owner/flats.html', types=types)


@owner.route('/lease', methods=['GET', 'POST'])
def lease():
    # agreeing to terms and conditions
    if request.method == 'POST':
        return redirect(url_for('.register')) 
    return render_template('owner/lease.html')


@owner.route('/renew_payment', methods=['GET', 'POST'])
@login_required
def renew_payment():
    return 'Renew payment here'


@owner.route('/signup', methods=['GET', 'POST'])
def signup():
    """The signup page for a new owner to enter their information for their profile."""
    form = RegisterResident()
    if form.validate_on_submit():
        try:
            user = User(
                fullname = form.fullname.data,
                email = form.email.data,
                number = int(form.number.data),
                password = form.password.data,
                # resident role is ID 1, no conflicts here
                role = form.role.data
                # account is only deactivated a certain time after lease is terminated
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
    return render_template('owner/register.html', form=form)


@owner.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('owner.index'))