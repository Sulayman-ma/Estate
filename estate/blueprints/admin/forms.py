from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    SelectField,
    BooleanField,
    PasswordField,
    EmailField,
    TelField,
    SubmitField,
    TextAreaField
)
from wtforms.validators import Email, EqualTo



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
        'AGENT', 'CLEANER'
    ])
    password = PasswordField(EqualTo('password2', message='Passwords must match'), render_kw={
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
    fullname = StringField(label="Full Name", render_kw={
        'placeholder': 'Full Name'
    })
    email = EmailField(label="E-mail", render_kw={'placeholder': 'Email'})
    number = TelField(label="Number", render_kw={
        'placeholder': 'Number'
    })
    role = SelectField(label="Role", choices=[
        'AGENT', 'CLEANER'
    ], render_kw = {'disabled': 'disabled'})
    is_active = BooleanField()
    save = SubmitField(label='Save Changes')


class Login(FlaskForm):
    """User login, applicable to all roles."""
    user_tag = StringField(label="Staff ID", render_kw={
        'placeholder': 'Staff ID',
        'required': 'required',
    })
    password = PasswordField(label="Password", render_kw={
        'placeholder': 'Password',
        'required': 'required',
    })
    login = SubmitField(label='Login', render_kw={
        'class': 'button-primary'
    })


class CreateFlatType(FlaskForm):
    name = StringField(label="Name", render_kw={
        'placeholder': 'Name',
        'required': 'required',
    })
    rent = TelField(label="Rent", render_kw={
      'placeholder': 'Rent Amount',
      'required': 'required'  
    })
    description = TextAreaField(label='Description', render_kw={
        'placeholder': 'The best flat for the ocean view lovers, comes with...',
        'required': 'required'
    })
    bedrooms = TelField(label='Bedrooms', render_kw={
        'placeholder': 'Number of Bedrooms',
        'required': 'required'
    })
    bathrooms = TelField(label='Bathrooms', render_kw={
        'placeholder': 'Number of Bathrooms',
        'required': 'required'
    })
    num_available = TelField(label='Available', render_kw={
        'placeholder': 'Number Available',
        'required': 'required'
    })
    create = SubmitField(label='Create', render_kw={
        'class': 'button-primary'
    })


class EditFlatType(FlaskForm):
    name = StringField(label="Name", render_kw={
        'placeholder': 'Name',
        'required': 'required',
    }, validators=[])
    rent = TelField(label="Rent", render_kw={
      'placeholder': 'Rent Amount',
      'required': 'required'  
    })
    description = TextAreaField(label='Description', render_kw={
        'placeholder': 'The best flat for the ocean view lovers, comes with...',
        'required': 'required'
    })
    bedrooms = TelField(label='Bedrooms', render_kw={
        'placeholder': 'Number of Bedrooms',
        'required': 'required'
    })
    bathrooms = TelField(label='Bathrooms', render_kw={
        'placeholder': 'Number of Bathrooms',
        'required': 'required'
    })
    num_available = TelField(label='Available', render_kw={
        'placeholder': 'Number Available',
        'required': 'required'
    })
    save = SubmitField(label='Save Changes', render_kw={
        'class': 'button-primary'
    })