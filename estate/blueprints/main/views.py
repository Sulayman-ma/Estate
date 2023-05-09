from . import main
from flask import render_template


@main.route('/')
@main.route('/index')
def index():
    return render_template('main/index.html')
