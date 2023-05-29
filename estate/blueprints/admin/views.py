from . import admin
from ... import db
from ...models import User, Role
from ...decorators import admin_required
from .forms import (
    RegisterStaff,
    Login,
    EditStaffInfo,
    CreateFlatType
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
@admin_required
def dash():
    # order staff in descending order of active status using `desc()`
    agents = User.get_users('agent').order_by(User.is_active.desc())
    cleaners = User.get_users('cleaner').count()
    
    total_staff = agents.count() + cleaners
    return render_template(
        'admin/dash.html', agents=agents, cleaners=cleaners, total_staff=total_staff
    )


# STAFF VIEWS
@admin.route('/admin/register_staff', methods=['GET', 'POST'])
@login_required
@admin_required
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
            # set to True in this view, default is false for any other view
            is_staff = True
        )
        staff.generate_user_tag()
        db.session.add(staff)
        db.session.commit()
        flash('Registration successful ✔', 'success')
        return redirect(url_for('.all_staff'))
    return render_template('admin/register_staff.html', form=form)


@admin.route('/admin/edit_staff/<int:id>', methods=['GET', 'POST', 'PUT'])
@login_required
@admin_required
def edit_staff(id):
    """All editing of staff info and changing of their active status"""
    user = User.query.get(id)
    form = EditStaffInfo(user=user)
    if form.is_submitted():
        user.fullname = form.fullname.data
        user.email = form.email.data
        user.is_active = form.is_active.data
        user.number = form.number.data
        db.session.commit()
        flash('Changes saved successfully ✔', 'success')
        return redirect(url_for('.edit_staff', id=id))
    form.fullname.data = user.fullname
    form.email.data = user.email
    form.number.data = user.number
    form.role.data  = Role.query.get(user.role_id).name
    form.is_active.data = user.is_active
    return render_template('admin/edit_staff.html', form=form)


@admin.route('/admin/all_staff')
@login_required
@admin_required
def all_staff():
    # specifying initial page
    page = request.args.get('page', 1, type=int)

    # order staff in order of active staff first using `desc()`
    staffs = User.get_users('staff').order_by(User.is_active.desc())

    # paginate merged staff queries
    # staffs = staffs.paginate(
    #     page=page, per_page=20, error_out=False
    # )
    return render_template('admin/all_staff.html', staffs=staffs)


@admin.route('/admin/residents')
@login_required
@admin_required
def residents():
    res = User.get_users('resident')
    return render_template('admin/residents.html', res=res)


@admin.route('/admin/payments/<int:id>')
@login_required
@admin_required
def payments(id):
    """View all payments made by a specific residet"""
    user = User.query.get(id)
    return render_template('admin/payments.html')


@admin.route('/admin/flats')
@login_required
@admin_required
def flats():
    return '<h2>Not Implemented</h2><p>Funcionality requires a prerequisite that is under development.</p>'


@admin.route('/admin/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        # login is only allowed with user tag
        user = User.query.filter_by(user_tag=form.user_tag.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=False)
            return redirect(url_for('.dash'))
        flash("shinji, admin [user tag, password]")
    return render_template('admin/login.html', form=form)


@admin.route('/admin/logout')
@login_required
@admin_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))