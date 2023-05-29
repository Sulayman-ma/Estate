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
from ...models import FlatType



class RegisterResident(FlaskForm):
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


class Login(FlaskForm):
    user_tag = StringField(render_kw={
        'placeholder': 'User Tag',
        'required': 'required',
    })
    password = PasswordField(render_kw={
        'placeholder': 'Password',
        'required': 'required',
    })
    login = SubmitField(label='Login', render_kw={
        'class': 'button-primary'
    })


class Agree(FlaskForm):
    check = BooleanField()
    proceed = SubmitField(label='AGREE TO TERMS & CONDITIONS', render_kw={
        'class': 'button-primary'
    })


class Pay(FlaskForm):
    pass
