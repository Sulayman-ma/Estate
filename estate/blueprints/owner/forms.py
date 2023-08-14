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



class RegisterOwner(FlaskForm):
    fullname = StringField(label="Full Name", render_kw={
        'placeholder': 'Full Name',
        'required': 'required',
    })
    email = EmailField(label="E-mail", render_kw={
        'placeholder': 'Email', 'required': 'required',
        }, validators=[Email()])
    number = TelField(label="Number", render_kw={
        'placeholder': 'Number',
        'required': 'required',
    })
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