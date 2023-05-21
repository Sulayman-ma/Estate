from . import admin
from ... import db
from ...models import User, Role
from .forms import (
    RegisterStaff,
    Login,
    EditStaffInfo
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
    agents = User.query.filter_by(role_id=2)
    cleaners = User.query.filter_by(role_id=3).count()
    
    total_staff = agents.count() + cleaners
    return render_template(
        'admin/dash.html', agents=agents, cleaners=cleaners, total_staff=total_staff
    )


# STAFF VIEWS
@admin.route('/admin/register_staff', methods=['GET', 'POST'])
@login_required
def register_staff():
    form = RegisterStaff()
    if form.validate_on_submit():
        staff = User(
            fullname = form.fullname.data,
            email = form.email.data,
            number = form.number.data,
            # assign with Role object
            role = Role.query.filter_by(name=form.role.data).first(),
            is_active = form.is_active.data,
        )
        staff.generate_user_tag()
        db.session.add(staff)
        db.session.commit()
        flash('Registration successful ✔', 'success')
        return redirect(url_for('.register_staff'))
    return render_template('admin/register_staff.html', form=form)


@admin.route('/admin/edit_staff/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_staff(id):
    """All editing of staff info and changing of their active status"""
    user = User.query.get_or_404(id)
    form = EditStaffInfo(user=user)
    if form.validate_on_submit():
        user.fullname = form.fullname.data
        user.email = form.email.data
        user.number = form.number.data
        # assign with Role object
        # user.role = Role.query.filter_by(name=form.role.data).first()
        user.is_active = form.is_active.data
        db.session.add(user)
        db.session.commit()
        flash('Changes saved successfully ✔', 'success')
        return redirect(url_for('.all_staff'))
    form.fullname.data = user.fullname
    form.email.data = user.email
    form.number.data = user.number
    form.role.data  = Role.query.get(user.role_id).name
    form.is_active.data = user.is_active
    return render_template('admin/edit_staff.html', form=form)


@admin.route('/admin/all_staff')
@login_required
def all_staff():
    # specifying initial page
    page = request.args.get('page', 1, type=int)

    # list of all staff query objects
    queries = User.get_users('staff')
    # use first query object as base
    staffs = queries.pop(0)
    for query in queries:
        # merge queries into one
        staffs = staffs.union(query)

    # paginate merged staff queries
    staffs = staffs.paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/all_staff.html', staffs=staffs)


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
        user = User.query.filter_by(user_tag=form.user_tag.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=False)
            return redirect(url_for('.dash'))
        flash("shinji, admin [user tag, password]")
    return render_template('admin/login.html', form=form)


@admin.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.dash'))