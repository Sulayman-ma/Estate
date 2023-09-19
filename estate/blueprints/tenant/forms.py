from flask_wtf import FlaskForm
from wtforms.fields import (
    SubmitField,
    IntegerField,
    PasswordField,
    SelectField
)
from wtforms.validators import (
    InputRequired
)



class MakePayment(FlaskForm):
    amount = IntegerField(label='Rent Amount', render_kw={
        'placeholder': 'Rent amount to pay'
    }, validators=[InputRequired()])
    status = SelectField(label='Payment Status', choices={
        'FULL', 'PARTIAL'
    }, validators=[InputRequired()])
    password = PasswordField(label='Password', render_kw={
        'placeholder': 'Please enter your password'
    }, validators=[InputRequired()])
    confirm = SubmitField(label='CONFIRM', render_kw={
        'class': 'button-primary'
    })