from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    SelectField,
    BooleanField,
    EmailField,
    TelField,
    SubmitField
)
from wtforms.validators import Email



class RegisterStaff(FlaskForm):
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
    role = SelectField(label="Role", choices=[
        'HANDYMAN', 'MANAGER'
    ])
    is_active = BooleanField()
    register = SubmitField(label='Register')


class EditStaffInfo(FlaskForm):
    fullname = StringField(label="Full Name", render_kw={
        'placeholder': 'Full Name'
    })
    email = EmailField(label="E-mail", render_kw={'placeholder': 'Email'})
    number = TelField(label="Number", render_kw={
        'placeholder': 'Number'
    })
    role = SelectField(label="Role", choices=[
        'HANDYMAN', 'MANAGER'
    ], render_kw = {'disabled': 'disabled'})
    is_active = BooleanField()
    save = SubmitField(label='Save Changes')