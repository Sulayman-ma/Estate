from . import main
from ... import db
from .forms import (
    RegisterResident, 
    Login, 
    Agree,
    Pay
)
from ...decorators import role_required
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
    request,
    current_app
)
from ...models import (
    User,
    Role,
    Payment,
    FlatType
)
from wtforms.validators import ValidationError
from datetime import datetime, timedelta



@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/profile')
@role_required('RESIDENT')
def profile():
    return render_template('main/profile.html')


@main.route('/flats')
def flats():
    types = FlatType.query.all()
    return render_template('main/flats.html', types=types)


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
        try:
            category = request.form.get('flat_type')
            flat_type = FlatType.query.filter_by(name=category).first()
            # process payment
            payment = Payment(
                amount = flat_type.rent,
                description = 'Resident {}, flat type {}'.format(current_user.user_tag, flat_type.name),
                timestamp = datetime.now(),
                user_id = current_user.id
            )
            db.session.add(payment)
            # update resident info
            lease_start = datetime.now()
            lease_duration = int(request.form.get('lease_duration'))
            current_user.lease_start = lease_start
            current_user.lease_duration = lease_duration
            current_user.lease_expiry = lease_start + timedelta(days=lease_duration*365)
            current_user.flattype_id = flat_type.id

            flat_type.num_available -= 1
            flat_type.update_status()

            db.session.add(current_user)
            db.session.commit()
            flash('Payment successful.', 'success')
            return redirect(url_for('.profile'))
        except ValueError:
            flash('⚠ Invalid input, please try again', 'error')
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


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('.profile'))
    form = Login()
    if form.validate_on_submit():
        # login is only allowed with user tag
        user = User.query.filter_by(user_tag=form.user_tag.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=True)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('.profile')
            return redirect(next)
            # return redirect(url_for('.profile'))
        flash('⚠ Incorrect details, ensure to use upper case for ID', 'error')
    return render_template('main/login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))