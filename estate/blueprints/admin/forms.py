from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    SelectField,
    BooleanField,
    EmailField,
    TelField,
    SubmitField,
    PasswordField,
    RadioField
)
from wtforms.validators import Email



class RegisterStaff(FlaskForm):
    first_name = StringField(label="First Name", render_kw={
        'placeholder': 'Firt Name',
        'required': 'required'
    })
    middle_name = StringField(label="Middle Name", render_kw={
        'placeholder': 'Middle Name'
    })
    last_name = StringField(label="Last Name", render_kw={
        'placeholder': 'Last Name',
        'required': 'required'
    })
    # gender = RadioField('Level', choices=[
    #     'Male', 'Female'
    # ])
    email = EmailField(label="E-mail", render_kw={
        'placeholder': 'Email', 
        'required': 'required',
    }, validators=[Email()])
    number = TelField(label="Number", render_kw={
        'placeholder': 'Number',
        'required': 'required',
    })
    role = SelectField(label="Role", choices=[
        'WORKER', 'MANAGER'
    ])
    is_active = BooleanField()
    register = SubmitField(label='Register')


class EditStaffInfo(FlaskForm):
    first_name = StringField(label="First Name", render_kw={
        'placeholder': 'Firt Name'
    })
    middle_name = StringField(label="Middle Name", render_kw={
        'placeholder': 'Middle Name'
    })
    last_name = StringField(label="Last Name", render_kw={
        'placeholder': 'Last Name'
    })
    user_tag = StringField(label="User Tag", render_kw={
        'placeholder': 'User Tag'
    })
    email = EmailField(label="E-mail", render_kw={
        'placeholder': 'Email'
    })
    number = TelField(label="Number", render_kw={
        'placeholder': 'Number'
    })
    role = SelectField(label="Role", choices=[
        'WORKER', 'MANAGER'
    ], render_kw = {'disabled': 'disabled'}
    )
    is_active = BooleanField()
    save = SubmitField(label='Save Changes')


class CreateUser(FlaskForm):
    email = EmailField(label="E-mail", render_kw={
        'placeholder': 'Email', 
        'required': 'required'
    }, validators=[Email()])
    password = PasswordField(label='Password', render_kw={
        'placeholder': 'Enter Password',
        'required': 'required'
    })
    role = SelectField(label="Role", choices=[
        'TENANT', 'OWNER'
    ])
    # is_staff = BooleanField()
    register = SubmitField(label='Create')