from . import tenant
from ... import db
from ...decorators import role_required
from ...models import Flat, User, Notice
from .forms import MakePayment
from datetime import datetime
from dateutil.relativedelta import relativedelta
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



@tenant.route('/tenant/profile')
@login_required
@role_required('TENANT')
def index():
    # redirect new users to signup page
    # if current_user.is_new:
        # direct new users to terms and conditions agreement
        # return redirect(url_for('.agreement'))
    # flash('hiiii its me flash', 'success')
    today = datetime.today().date()
    flats = current_user.flats.all()
    for flat in flats:
        flat.check_expiry()
    return render_template('tenant/profile.html', today=today, flats=flats)


@tenant.route('/tenant/agreement/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('TENANT')
def agreement(id: int):
    """Terms and Conditions agreement for securing a lease.
    
    Keyword arguments:
    id -- Flat id
    Return: Agreement template and redirect to the rent payment page.
    """
    flat = Flat.query.get(id)
    today = datetime.today().date()
    # agreeing to terms and conditions when securing lease
    if request.method == 'POST' and request.form.get('agree') is not None:
        # redirect to profile completion for new users
        return redirect(url_for('.pay_rent', id=id))
    return render_template('tenant/agreement.html', flat=flat, today=today)


@tenant.route('/tenant/bulletin')
@login_required
@role_required('TENANT')
def bulletin():
    """ Show list of all notices for Tenants """
    notices = Notice.query.filter_by(target='TENANTS').all()
    return render_template('shared/bulletin.html', notices=notices)


@tenant.route('/tenant/flats_for_rent')
@login_required
@role_required('TENANT')
def flats_for_rent():
    """ Display all flats available for rent. """
    flats = Flat.query.all()
    return render_template('tenant/flats_for_rent.html', flats=flats)


@tenant.route('/tenant/terminate/<int:id>')
@login_required
@role_required('TENANT')
def terminate(id):
    """ Terminate lease. """
    flat = Flat.query.get(id)
    current_user.flats.remove(flat)
    db.session.commit()
    flash('Lease terminated for Block {}, Flat {}'.format(flat.block, flat.number))
    return redirect(url_for('.index'))


@tenant.route('/tenant/pay_rent/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('TENANT')
def pay_rent(id: int):
    """Authenticate user, initialize transaction and redirect user to the authorization URL to make the paymenet. Callback is the `renew_rent` view function.

    Tenant can pay in full or partially
    
    Keyword arguments:
    id -- Flat id
    Return: Pay Rent template and redirect to authorization URL.
    """
    flat = Flat.query.get(id)
    rent = flat.rent
    form = MakePayment()
    if form.validate_on_submit():
        if current_user.check_password(form.password.data) is False:
            flash('Incorrect password', 'error')
            return redirect(url_for('.pay_rent', id=id))
        # validate rent amount to ensure it is within bounds
        if form.amount.data > flat.rent:
            flash('Rent cannot exceed the agreed upon price of ₦ {:,}'.format(flat.rent), 'warning')
            return redirect(url_for('.pay_rent', id=id))
        # paystack transaction object
        transaction = current_app.config.get('API_OBJECT')
        # initialize transaction
        response = transaction.initialize(
            email = current_user.email,
            amount = form.amount.data * 100,
            label = current_user.username,
            callback_url = url_for(endpoint='.renew_rent', id=id, _external=True)
        )
        session['reference'] = response.get('reference')
        # session['payment_status'] = form.status.data
        session['payment_amount'] = form.amount.data
        # redirect user to payment url 
        return redirect(response.get('authorization_url'))
    return render_template('tenant/pay_rent.html', form=form, rent=rent, flat=flat)


@tenant.route('/tenant/renew_rent/<int:id>')
@login_required
@role_required('TENANT')
def renew_rent(id: int):
    """Rewews tenant rent and sets all appropriate properties on both the users's record and the flat's record.
    
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
        # set overdue rent amount
        amount = session.pop('payment_amount')
        flat.rent_overdue -= amount

        # payment_status = session.pop('payment_status')

        # create payment record
        # payment = Payment(
        #     type = 'rent',
        #     amount = amount,
        #     status = payment_status,
        #     username = current_user.username,
        #     flat_id = id
        # )
        # db.session.add(payment)

        # if lease is new, set new lease start date and expiry
        if flat not in current_user.flats.all():
            current_user.flats.add(flat)
            flat.lease_start = datetime.today()
            flat.lease_expiry = flat.lease_start + relativedelta(years=1)
        # else extend rent expiry upon full payment
        if flat.rent_overdue == 0:
            flat.lease_expiry = flat.lease_expiry + relativedelta(years=1)
        db.session.commit()
        session.pop('reference')
        flash('Payment successful ✔', 'success')
        return redirect(url_for('.index'))
    else:
        session.pop('reference')
        # session.pop('payment_status')
        session.pop('payment_amount')
        flash('Payment failed ❌', 'error')
        return redirect(url_for('.index'))