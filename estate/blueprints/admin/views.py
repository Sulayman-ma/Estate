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
        return redirect(url_for('.all_staff'))
    return render_template('admin/register_staff.html', form=form)


@admin.route('/admin/edit_staff/<int:id>', methods=['GET', 'POST', 'PUT'])
@login_required
@admin_required
def edit_staff(id):
    """All editing of staff info and changing of their active status"""
    user = User.query.get(id)
    form = EditStaffInfo(user=user)
    return render_template('admin/edit_staff.html', form=form)


@admin.route('/admin/payments')
@login_required
@admin_required
def payments():
    return render_template('admin/payments.html')


@admin.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))