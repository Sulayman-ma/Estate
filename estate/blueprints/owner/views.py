from . import owner
from .forms import ModifyFlat, ConfirmPassword
from ... import db
from ...decorators import role_required
from ...models import (
    User,
    Flat,
    Notice
)
from flask_login import (
    login_required,
    current_user
)
from flask import (
    render_template, 
    redirect,
    url_for,
    flash,
    request,
    current_app,
    session
)
from sqlalchemy.exc import IntegrityError
from wtforms import ValidationError
from datetime import datetime



@owner.route('/owner/profile')
@login_required
@role_required('OWNER')
def index():
    # redirect new users to signup page
    # if current_user.is_new:
        # direct new users to terms and conditions agreement
        # return redirect(url_for('.agreement'))
    # flash('hiiii its me flash', 'success')
    flats = current_user.flats.all()
    today = datetime.today().date()
    return render_template('owner/profile.html', flats=flats, today=today)


@owner.route('/owner/agreement/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('OWNER')
def agreement(id):
    flat = Flat.query.get(id)
    today = datetime.today().date()
    # agreeing to terms and conditions and stuff
    if request.method == 'POST' and request.form.get('agree') is not None:
        # redirect to profile completion for new users
        return redirect(url_for('.buy_flat', id=id))
    return render_template('owner/agreement.html', flat=flat, today=today)


@owner.route('/owner/bulletin')
@login_required
@role_required('OWNER')
def bulletin():
    """ Show list of all notices for Tenants """
    notices = Notice.query.filter_by(target='OWNERS').all()
    return render_template('shared/bulletin.html', notices=notices)


@owner.route('/owner/modify_flat/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('OWNER')
def modify_flat(id):
    flat = Flat.query.get(id)
    form = ModifyFlat(obj=flat)
    if form.is_submitted():
        try:
            flat.rent = form.rent.data
            if flat.get_tenant() and not form.for_rent.data:
                flash('Flat has an active tenant ⚠', 'warning')
                return redirect(url_for('.modify_flat', id=id))
            flat.for_rent = form.for_rent.data
            flat.for_sale = form.for_sale.data
            flat.cost = form.cost.data
            flat.description = form.description.data
            flat.payment_freq = form.payment_freq.data
            db.session.commit()
            return redirect(url_for('.index'))
        except ValidationError:
            flash('Invalid input(s), please check the fields again.', 'error')
            return redirect(url_for('.modify_flat', id=id))
        except IntegrityError:
            flash('Invalid input(s), please check the fields again.', 'error')
            return redirect(url_for('.modify_flat', id=id))
        except:
            flash('⚠ An error has occured, please contact the dev if error persists.', 'error')
            return redirect(url_for('.modify_flat', id=id))
    return render_template('owner/modify_flat.html', form=form)


@owner.route('/owner/flats_on_sale')
@login_required
@role_required('OWNER')
def flats_on_sale():
    """ Buy now button is here, `buy_flat` function carries out the process. The gateway module will also be used in the view function below. """
    flats = Flat.query.all()
    return render_template('owner/flats_on_sale.html', flats=flats)


@owner.route('/owner/buy_flat/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('OWNER')
def buy_flat(id):
    """Authenticate user, initialize transaction and redirect user to the authorization URL to make the paymenet. Callback is the `set_flat` view function.

    Buyers interested can only pay in full. Callback url is the set_flat view for setting necessary properties and making the required additions.
    
    Keyword arguments:
    id -- Flat id
    Return: Buy Flat template and redirect to authorization URL.
    """
    form = ConfirmPassword()
    flat = Flat.query.get(id)
    if form.validate_on_submit():
        # on incorrect password
        if not current_user.check_password(form.password.data):
            flash('Incorrect password', 'error')
            return redirect(url_for('.buy_flat', id=id))
        # paystack transaction object
        transaction = current_app.config.get('API_OBJECT')
        # initialize transaction
        response = transaction.initialize(
            email = current_user.email,
            amount = flat.cost * 100,
            label = current_user.username,
            callback_url = url_for(endpoint='.set_flat', id=id, _external=True)
        )
        session['reference'] = response.get('reference')
        # redirect user to payment url 
        return redirect(response.get('authorization_url'))
    return render_template('owner/buy_flat.html', form=form)


@owner.route('/owner/set_flat/<int:id>')
@login_required
@role_required('OWNER')
def set_flat(id):
    """Set flat function for creating the Payment record and assigning user to Flat. Also chang attributes of Flat being purchased.
    
    Keyword arguments:
    id -- Flat id
    Return: Redirect to user profile
    """
    flat = Flat.query.get(id)
    # check the status of the transaction
    transaction = current_app.config.get('API_OBJECT')
    status = transaction.verify(session.get('reference'))
    # if payment was successful, proceed to set
    if status is True:
        session.pop('reference')
        # create payment record
        # payment = Payment(
        #     type = 'buy',
        #     amount = flat.cost,
        #     status = 'full',
        #     username = current_user.username,
        #     flat_id = flat.id
        # )
        # db.session.add(payment)

        # sets flat fields appropriately
        flat.for_rent = False
        flat.for_sale = False
        flat.cost = 0
        current_user.flats.add(flat)
        db.session.commit()
        flash('Payment successful ✔', 'success')
        return redirect(url_for('.index'))
    else:
        session.pop('reference')
        flash('Payment failed ❌', 'error')
        return redirect(url_for('.index'))
