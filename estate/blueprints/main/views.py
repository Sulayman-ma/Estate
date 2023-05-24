from . import main
from ..admin.forms import Login
from flask_login import (
    login_required,
    logout_user,
    login_user
)
from flask import (
    render_template, 
    redirect,
    url_for,
    flash,
    request,
    current_app
)
from ...models import (
    User,
    Role,
    Payment,
    FlatType,
    Flat
)
import secrets



@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/profile')
@login_required
def profile():
    return '<h2>Not Implemented</h2><p>Funcionality requires a prerequisite that is under development.</p>'


@main.route('/flats')
def flats():
    types = FlatType.query.all()
    return render_template('main/flats.html', types=types)


@main.route('/lease', methods=['GET', 'POST'])
def lease():
    # TODO: payment logic 
    if request.method == 'POST':
        return redirect(url_for('.pay_and_register')) 
    return render_template('main/lease.html')


@main.route('/pay_and_register')
@login_required
def pay_and_register():
    """Register user and make payment. Redirected from .lease view"""
    return '<h2>Not Implemented</h2><p>Funcionality requires a prerequisite that is under development.</p>'


@main.route('/login')
def login():
    form = Login()
    if form.validate_on_submit():
        pass
    return '<h2>Not Implemented</h2><p>Funcionality requires a prerequisite that is under development.</p>'


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))