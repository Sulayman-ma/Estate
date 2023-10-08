from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    SelectField,
    BooleanField,
    EmailField,
    TelField,
    SubmitField,
    PasswordField,
    TextAreaField
)
from wtforms.validators import Email



class RegisterStaff(FlaskForm):
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
        'PLUMBER', 'ELECTRICIAN', 'MANAGER', 'SECURITY', 'CLEANER'
    ])
    is_active = BooleanField()
    register = SubmitField(label='Register')


class EditStaffInfo(FlaskForm):
    first_name = StringField(label="First Name", render_kw={
        'placeholder': 'First Name'
    })
    middle_name = StringField(label="Middle Name", render_kw={
        'placeholder': 'Middle Name'
    })
    last_name = StringField(label="Last Name", render_kw={
        'placeholder': 'Last Name'
    })
    username = StringField(label="Username", render_kw={
        'placeholder': 'Username'
    })
    email = EmailField(label="E-mail", render_kw={
        'placeholder': 'Email'
    })
    number = TelField(label="Number", render_kw={
        'placeholder': 'Number'
    })
    role = SelectField(label="Role", choices=[
        'PLUMBER', 'ELECTRICIAN', 'MANAGER', 'SECURITY', 'CLEANER'
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
    create = SubmitField(label='Create')


class SendNotice(FlaskForm):
    subject = StringField(label="Subjct", render_kw={
        'placeholder': 'Message Subject',
        'required': 'required'
    }, description='Something random?')
    message = TextAreaField(label='Notice Message', render_kw={
        'placeholder': 'Type notice message...',
        'required': 'required'
    })
    target = SelectField(label='Target Users', choices={
        'ALL', 'TENANTS', 'OWNERS'
    })
    mail = BooleanField()
    send = SubmitField(label='Send Notice')