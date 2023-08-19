from . import owner
from .forms import ModifyFlat
from ... import db
from ...decorators import role_required
from ...models import Flat
from flask_login import (
    login_required,
    current_user
)
from flask import (
    render_template, 
    redirect,
    url_for,
    flash,
    request
)
from sqlalchemy.exc import IntegrityError
from wtforms import ValidationError



@owner.route('/owner/profile')
@login_required
@role_required('OWNER')
def index():
    # redirect new users to signup page
    if current_user.is_new:
        # direct new users to terms and conditions agreement
        return redirect(url_for('.agreement'))
    return render_template('owner/profile.html')


@owner.route('/owner/agreement', methods=['GET', 'POST'])
@login_required
@role_required('OWNER')
def agreement():
    # agreeing to terms and conditions and stuff
    if request.method == 'POST' and request.form.get('agree') is not None:
        # redirect to profile completion for new users
        return redirect(url_for('auth.edit_profile', id=current_user.id))
    else:
        flash('Please accept the terms and conditions before proceeding.', 'misc')
    return render_template('owner/agreement.html')


@owner.route('/owner/modify_flat/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('OWNER')
def modify_flat(id):
    flat = Flat.query.get(id)
    form = ModifyFlat(obj=flat)
    if form.is_submitted():
        try:
            flat.rent = form.rent.data
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
    flat = Flat.query.get(id)
    """ NO TEMPLATE VIEW FUNCTION
    Permanent implementation will be that of processing the payments with the gateway and then carrying out the rest of the logic as shown below. 
    
    As a temporary implementation, when an owner buys a flat, its rent and sale status are set to False and cost amount is reset to 0. 
    The owner can modify these attributes in their profile at their convenience. """
    flat.for_rent = False
    flat.for_sale = False
    flat.cost = 0
    current_user.flats.add(flat)
    db.session.commit()
    return redirect(url_for('.index'))
