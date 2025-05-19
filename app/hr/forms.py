from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional
from app.models import Store

class EmployeeForm(FlaskForm):
    first_name = StringField('Όνομα', validators=[DataRequired()])
    last_name = StringField('Επώνυμο', validators=[DataRequired()])
    father_name = StringField('Πατρώνυμο', validators=[Optional()])
    age = IntegerField('Ηλικία', validators=[Optional()])
    vat = StringField('ΑΦΜ', validators=[Optional()])
    amka = StringField('ΑΜΚΑ', validators=[Optional()])
    telephone = StringField('Τηλέφωνο', validators=[Optional()])
    address = StringField('Διεύθυνση', validators=[Optional()])
    iban = StringField('IBAN', validators=[Optional()])
    ama = StringField('ΑΜΑ', validators=[Optional()])
    store_id = SelectField('Κατάστημα', coerce=int, validators=[Optional()])
    submit = SubmitField('Αποθήκευση')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.store_id.choices = [(s.id, s.name) for s in Store.query.order_by(Store.name).all()]

class DeleteForm(FlaskForm):
    pass  # Μόνο για CSRF προστασία        