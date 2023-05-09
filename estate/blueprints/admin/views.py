from . import admin
from .forms import Login
from ...models import(
    Staff,
    Admin,
    Resident,
    Payment,
    Role
)
from flask import(
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
@login_required
def dash():
    # staff displayed are limited to agents only
    agents = Staff.query.filter_by(role_id=1)
    managers = Staff.query.filter_by(role_id=2)
    cleaners = Staff.query.filter_by(role_id=3)
    
    total_staff = len(Staff.query.all())
    return render_template(
        'admin/dash.html', agents=agents, managers=managers, cleaners=cleaners, total_staff=total_staff
    )


# STAFF VIEWS
@admin.route('/admin/register_staff')
@login_required
def register_staff():
    return render_template('admin/register_staff.html')


@admin.route('/admin/all_staff')
@login_required
def all_staff():
    # specifying initial page
    page = request.args.get('page', 1, type=int)
    # using pagination method because why not?
    staffs = Staff.query.paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/all_staff.html', staffs=staffs)


@admin.route('/admin/edit_staff')
@login_required
def edit_staff():
    """All editing of staff info and changing of their active status"""
    return render_template('admin/edit_staff.html')


@admin.route('/admin/residents')
@login_required
def residents():
    pass


@admin.route('/admin/payments')
@login_required
def payments():
    pass


@admin.route('/admin/flats')
@login_required
def flats():
    pass


@admin.route('/admin/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(admin_id=form.admin_id.data).first()
        if admin is not None and admin.check_password(form.password.data):
            login_user(admin, remember=False)
            return redirect(url_for('.dash'))
        flash('Access denied', 'warning')
    return render_template('admin/login.html', form=form)


@admin.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.dash'))