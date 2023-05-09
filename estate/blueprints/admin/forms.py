from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    SelectField,
    BooleanField,
    PasswordField,
    EmailField,
    TelField,
    SubmitField
)
from wtforms.validators import InputRequired, Email



class RegisterStaff(FlaskForm):
    pass


class EditStaffInfo(FlaskForm):
    pass


class Login(FlaskForm):
    admin_id = StringField(render_kw={
        'placeholder': 'Admin ID',
        'required': 'required',
        'class': []
    })
    password = PasswordField(render_kw={
        'placeholder': 'Password',
        'required': 'required',
        'class': []
    })
    login = SubmitField(label='Login')