from . import admin
from ... import db
from ...models import (
    User,
    Role,
    Payment,
    FlatType,
    Flat
)
from ...decorators import admin_required
from .forms import (
    RegisterStaff,
    EditStaffInfo
)
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from flask_login import (
    login_user, 
    logout_user, 
    login_required
)



@admin.route('/dash')
def dash():
    managers = User.query.filter_by(role_id=2)
    handymen = User.query.filter_by(role_id=4)

    staff = managers.union(handymen)
    return render_template('admin/dash.html')


# STAFF VIEWS
@admin.route('/admin/register_staff', methods=['GET', 'POST'])
def register_staff():
    form = RegisterStaff()
    return render_template('admin/register_staff.html', form=form)


# @admin.route('/admin/edit_staff/<int:id>', methods=['GET', 'POST', 'PUT'])
# def edit_staff(id):
#     """All editing of staff info and changing of their active status"""
#     user = User.query.get(id)
#     form = EditStaffInfo(user=user)
#     return render_template('admin/edit_staff.html', form=form)


@admin.route('/admin/all_staff')
def all_staff():
    return render_template('admin/all_staff.html')


@admin.route('/admin/residents')
def residents():
    return render_template('admin/residents.html')


@admin.route('/admin/payments')
def payments():
    """View all payments made by a specific residet"""
    return render_template('admin/payments.html')


@admin.route('/admin/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))