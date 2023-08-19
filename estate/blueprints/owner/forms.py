from flask_wtf import FlaskForm
from wtforms.fields import (
    BooleanField,
    SubmitField,
    IntegerField,
    TextAreaField
)
from wtforms.validators import (
    InputRequired
)



class ModifyFlat(FlaskForm):
    for_sale = BooleanField()
    cost = IntegerField(label="Sale Cost", render_kw={
        'placeholder': 'Sale Cost'
    })
    for_rent = BooleanField()
    rent = IntegerField(label="Rent Cost", render_kw={
        'placeholder': 'Rent Cost'
    }, validators=[InputRequired()])
    payment_freq = IntegerField(label="Payment Frequency", render_kw={
        'placeholder': 'Payment Frequency (in months)'
    }, validators=[InputRequired()])
    description = TextAreaField(label="Description", render_kw={
        'placeholder': 'Details about the flat, its current state and any additional info...'
    })
    save = SubmitField(label='Save Changes')