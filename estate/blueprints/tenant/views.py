from . import tenant
from ... import db
from ...decorators import role_required
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



@tenant.route('/tenant/profile')
@login_required
@role_required('TENANT')
def index():
    # redirect new users to signup page
    if current_user.is_new:
        # direct new users to terms and conditions agreement
        return redirect(url_for('.agreement'))
    return render_template('tenant/profile.html')


@tenant.route('/tenant/agreement', methods=['GET', 'POST'])
@login_required
@role_required('TENANT')
def agreement():
    # agreeing to terms and conditions and stuff
    if request.method == 'POST' and request.form.get('agree') is not None:
        # redirect to profile completion for new users
        return redirect(url_for('auth.edit_profile', id=current_user.id))
    return render_template('tenant/agreement.html')


@tenant.route('/tenant/renew_payment', methods=['GET', 'POST'])
@login_required
@role_required('TENANT')
def renew_payment():
    return 'Renew payment here'