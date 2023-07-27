from . import admin
from ... import db
from ...decorators import admin_required
from ...models import (
    User,
    Role,
    Payment
)
from .forms import (
    RegisterStaff,
    EditStaffInfo
)
from flask import (
    render_template,
    redirect,
    url_for,
    flash
)
from flask_login import (
    logout_user, 
    login_required
)



@admin.route('/dash')
@login_required
@admin_required
def dash():
    return render_template('admin/dash.html')


@admin.route('/admin/all_staff')
@login_required
@admin_required
def all_staff():
    staff = User.get_users('staff')
    return render_template('admin/all_staff.html', staff=staff)


@admin.route('/admin/register_staff', methods=['GET', 'POST'])
@login_required
@admin_required
def register_staff():
    form = RegisterStaff()
    if form.validate_on_submit():
        # create user, generate tag and add to database
        role = Role.query.filter_by(name=form.role.data).first()
        staff = User(
            fullname = form.fullname.data,
            email = form.email.data,
            number = form.number.data,
            role = role
        )
        staff.generate_user_tag()
        db.session.add(staff)
        db.session.commit()
        flash('Staff member added ✔', 'success')
        return redirect(url_for('.all_staff'))
    return render_template('admin/register_staff.html', form=form)


@admin.route('/admin/edit_staff/<int:id>', methods=['GET', 'POST', 'PUT'])
@login_required
@admin_required
def edit_staff(id):
    """All editing of staff info and changing of their active status"""
    user = User.query.get(id)
    # fill form with current user data by passing `obj` parameter
    form = EditStaffInfo(obj=user)
    if form.is_submitted():
        # apply changes made to user model
        user.fullname = form.fullname.data
        user.email = form.email.data
        user.number = form.number.data
        user.is_active = form.is_active.data
        db.session.commit()
        flash('Changes applied ✔', 'success')
        return redirect(url_for('.all_staff'))
    return render_template('admin/edit_staff.html', form=form)


@admin.route('/admin/payments')
@login_required
@admin_required
def payments():
    payments = Payment.query.all()
    # TODO: paginate the payments

    # TODO: provide filters for search by; user, 
    return render_template('admin/payments.html', payments=payments)


@admin.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))