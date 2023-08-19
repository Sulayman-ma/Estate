from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    PasswordField,
    EmailField,
    TelField,
    SubmitField
)
from wtforms.validators import Email



class EditProfile(FlaskForm):
    username = StringField(label="Username", render_kw={
        'placeholder': 'Username',
        'required': 'required'
    })
    first_name = StringField(label="First Name", render_kw={
        'placeholder': 'First Name',
        'required': 'required'
    })
    middle_name = StringField(label="Middle Name", render_kw={
        'placeholder': 'Middle Name'
    })
    last_name = StringField(label="Last Name", render_kw={
        'placeholder': 'Last Name',
        'required': 'required'
    })
    email = EmailField(label="E-mail", render_kw={
        'placeholder': 'Email', 'disabled':'disabled'
        }, validators=[Email()])
    number = TelField(label="Number", render_kw={
        'placeholder': 'Number',
        'required': 'required'
    })
    # TODO: add remaining fields common to both users
    # old_password = PasswordField(render_kw={
    #     'placeholder': 'Old Password'
    # })
    new_password = PasswordField(render_kw={
        'placeholder': 'New Password'
    })
    save = SubmitField(label='Save Changes')