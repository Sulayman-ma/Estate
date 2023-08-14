from . import admin
from ... import db
from ...decorators import admin_required
from ...models import (
    User,
    Payment,
    Flat
)
from .forms import (
    RegisterStaff,
    EditStaffInfo,
    CreateUser
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
from sqlalchemy.exc import IntegrityError



@admin.route('/admin/dash')
@login_required
@admin_required
def index():
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
        try:
            # create user, generate tag and add to database
            staff = User(
                first_name = form.first_name.data,
                middle_name = form.middle_name.data,
                last_name = form.last_name.data,
                email = form.email.data,
                number = form.number.data,
                role = form.role.data,
                is_staff = True
            )
            db.session.add(staff)
            # usernames are automatically generated and can be modified
            staff.generate_tag()
            db.session.commit()
        except IntegrityError:
            flash('⚠ User already exists. Use a different email if problem persists.', 'misc')
            return redirect(url_for('.register_staff'))
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
        try:
            user.first_name = form.first_name.data
            user.middle_name = form.middle_name.data
            user.last_name = form.last_name.data
            user.user_tag = form.user_tag.data
            user.email = form.email.data
            user.number = form.number.data
            user.is_active = form.is_active.data
            # db.session.add(user)
            db.session.commit()
        # for conflicts in unique fields; user tag and email
        except IntegrityError:
            flash('⚠ Email or user tag is already taken.', 'misc')
            return redirect(url_for('.edit_staff', id=id))
        flash('Changes applied ✔', 'success')
        return redirect(url_for('.all_staff'))
    return render_template('admin/edit_staff.html', form=form)


@admin.route('/admin/payments')
@login_required
@admin_required
def payments():
    payments = Payment.query.all()
    # TODO: paginate the payments

    # TODO: provide filters for search by; user tag, date/dates range
    return render_template('admin/payments.html', payments=payments)


@admin.route('/admin/flats')
@login_required
@admin_required
def flats():
    flats = Flat.query.all()
    # TODO: paginate the flats per block, to have 64 pages, easier that a search filter

    # TODO: provide filters for search by; user tag, block
    return render_template('admin/flats.html', flats=flats)


@admin.route('/admin/create_user')
@login_required
@admin_required
def create_user():
    """Admins collect the owner's or tenant's emails and passowrd and uses them to generate a user tag. 
    This user tag is then given to them to complete the signup and gain access to their respective profiles."""
    form = CreateUser()
    if form.validate_on_submit():
        try:
            user = User(
                email=form.email.data, 
                password=form.password.data, 
                role = form.role.data
            )
            user.generate_tag()
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            flash('⚠ Email already used.', 'misc')
            return redirect(url_for('.create_user'))
        flash('{} created successfully ✔. User Tag is {}'.format(user.role, user.user_tag))
        return redirect(url_for('.{}'.format(user.role.lower())))
    return render_template('admin/create_user.html', form=form)


@admin.route('/admin/tenants')
@login_required
@admin_required
def tenants():
    tenants = User.get_users('tenant')
    return render_template('admin/tenants.html', tenants=tenants)


@admin.route('/admin/owners')
@login_required
@admin_required
def owners():
    owners = User.get_users('owner')
    return render_template('admin/owners.html', owners=owners)


@admin.route('/admin/logout')
@login_required
@admin_required
def logout():
    logout_user()
    return redirect(url_for('login'))