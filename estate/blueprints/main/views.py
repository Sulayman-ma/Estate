from . import main
from ..admin.forms import Login
from flask_login import login_user, login_required
from flask import (
    render_template, 
    redirect,
    url_for,
    flash
)



@main.route('/')
@main.route('/index')
def index():
    return render_template('main/index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('main/profile.html')


# @main.route('/login')
# def login():
#     form = Login()
#     if form.validate_on_submit():
#         resident = Resident.query.filter_by(resident_id=form.user_id.data).first()
#         if resident is not None and resident.check_password(form.password.data):
#             login_user(resident, remember=True)
#             return redirect(url_for('.profile'))
#         flash('Incorrect login details', 'warning')
#     return render_template('main/login')