from . import admin
from ... import db
from ...decorators import role_required
from ...models import (
    User,
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
    login_required
)
from sqlalchemy.exc import IntegrityError
from wtforms import ValidationError
from datetime import datetime



@admin.route('/admin/dash')
@login_required
@role_required('ADMIN')
def index():
    return render_template('admin/dash.html')


@admin.route('/admin/all_staff')
@login_required
@role_required('ADMIN')
def all_staff():
    staff = User.get_users('staff')
    return render_template('admin/all_staff.html', staff=staff)


@admin.route('/admin/register_staff', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN')
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
            # initial usernames are automatically generated
            db.session.commit()
        except ValidationError:
            flash('Invalid input, please check all fields.', 'error')
            return redirect(url_for('.register_staff'))
        except IntegrityError:
            flash('⚠ Email already taken', 'misc')
            return redirect(url_for('.register_staff'))
        except:
            flash('⚠ An error has occured, please contact the dev if error persists.', 'error')
            return redirect(url_for('.register_staff'))
        flash('Staff member added ✔', 'success')
        return redirect(url_for('.all_staff'))
    return render_template('admin/register_staff.html', form=form)


@admin.route('/admin/edit_staff/<int:id>', methods=['GET', 'POST', 'PUT'])
@login_required
@role_required('ADMIN')
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
            user.username = form.username.data
            user.email = form.email.data
            user.number = form.number.data
            user.is_active = form.is_active.data
            # db.session.add(user)
            db.session.commit()
        # for conflicts in unique fields; Username and email
        except ValidationError:
            flash('Invalid input, please check all fields.', 'error')
            return redirect(url_for('.edit_staff', id=id))
        except IntegrityError:
            flash('⚠ Email or Username is already taken.', 'misc')
            return redirect(url_for('.edit_staff', id=id))
        except:
            flash('⚠ An error has occured, please contact the dev if error persists.', 'error')
            return redirect(url_for('.edit_staff', id=id))
        flash('Changes applied ✔', 'success')
        return redirect(url_for('.all_staff'))
    return render_template('admin/edit_staff.html', form=form)


@admin.route('/admin/payments')
@login_required
@role_required('ADMIN')
def payments():
    # payments = Payment.query.all()
    # TODO: paginate the payments

    # TODO: provide filters for search by; Username, date/dates range
    return render_template('admin/payments.html', payments=payments)


@admin.route('/admin/flats')
@login_required
@role_required('ADMIN')
def flats():
    flats = Flat.query.all()
    # TODO: paginate the flats per block, to have 64 pages, easier than a search filter

    # TODO: provide filters for search by; Username, block
    return render_template('admin/flats.html', flats=flats)


@admin.route('/admin/create_user', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN')
def create_user():
    """Admins collect the owner's or tenant's emails and passowrd and uses them to generate a Username. 
    This Username is then given to them to complete the signup and gain access to their respective profiles."""
    form = CreateUser()
    if form.validate_on_submit():
        try:
            user = User(
                email=form.email.data, 
                password=form.password.data, 
                role = form.role.data
            )
            # user.generate_tag()
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            flash('⚠ Email already taken', 'misc')
            return redirect(url_for('.create_user'))
        except:
            flash('⚠ An error has occured, please contact the dev if error persists.', 'error')
            return redirect(url_for('.create_user'))
        flash('{} created successfully ✔.'.format(user.role), 'success')
        return redirect(url_for('.{}s'.format(user.role.lower())))
    return render_template('admin/create_user.html', form=form)


@admin.route('/admin/tenants')
@login_required
@role_required('ADMIN')
def tenants():
    tenants = User.get_users('tenant')
    # TODO: paginate the template
    # TODO: add filters for search
    return render_template('admin/tenants.html', tenants=tenants, year=datetime.today().year)


@admin.route('/admin/owners')
@login_required
@role_required('ADMIN')
def owners():
    owners = User.get_users('owner')
    # TODO: paginate the template
    # TODO: add filters for search
    return render_template('admin/owners.html', owners=owners)