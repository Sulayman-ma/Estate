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
from wtforms.validators import Email, EqualTo



class RegisterStaff(FlaskForm):
    fullname = StringField(render_kw={
        'placeholder': 'Full Name',
        'required': 'required',
    })
    email = EmailField(render_kw={
        'placeholder': 'Email', 'required': 'required',
        }, validators=[Email()])
    number = TelField(render_kw={
        'placeholder': 'Number',
        'required': 'required',
    })
    role = SelectField(choices=[
        'AGENT', 'CLEANER'
    ])
    password = PasswordField(EqualTo('password2', message='Passwords must match'),render_kw={
        'placeholder': 'Password',
        'required': 'required',
    })
    password2 = PasswordField(render_kw={
        'placeholder': 'Confirm Password',
        'required': 'required',
    })
    is_active = BooleanField()
    register = SubmitField(label='Register')


class EditStaffInfo(FlaskForm):
    fullname = StringField(render_kw={
        'placeholder': 'Full Name'
    })
    email = EmailField(render_kw={'placeholder': 'Email'}, validators=[Email()])
    number = TelField(render_kw={
        'placeholder': 'Number'
    })
    role = SelectField(choices=[
        'AGENT', 'CLEANER'
    ], render_kw = {'disabled': 'disabled'})
    is_active = BooleanField()
    save = SubmitField(label='Save Changes')


class Login(FlaskForm):
    user_tag = StringField(render_kw={
        'placeholder': 'User Tag',
        'required': 'required',
    })
    password = PasswordField(render_kw={
        'placeholder': 'Password',
        'required': 'required',
    })
    login = SubmitField(label='Login')