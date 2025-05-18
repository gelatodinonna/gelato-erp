# app/stores/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class StoreForm(FlaskForm):
    name = StringField('Όνομα Καταστήματος', validators=[DataRequired(), Length(max=100)])
    location = StringField('Τοποθεσία', validators=[Length(max=200)])
    submit = SubmitField('Αποθήκευση')