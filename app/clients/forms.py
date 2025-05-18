# app/clients/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional

class ClientForm(FlaskForm):
    name = StringField('Όνομα Πελάτη', validators=[DataRequired()])
    vat_number = StringField('ΑΦΜ', validators=[Optional()])
    address = StringField('Διεύθυνση', validators=[Optional()])
    phone = StringField('Τηλέφωνο', validators=[Optional()])
    email = StringField('Email', validators=[Optional()])
    submit = SubmitField('Αποθήκευση')