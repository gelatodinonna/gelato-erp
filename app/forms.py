from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, Optional
from app.models import Store, Personnel

class StoreForm(FlaskForm):
    name = StringField('Όνομα Καταστήματος', validators=[DataRequired()])
    location = StringField('Τοποθεσία', validators=[Optional()])
    submit = SubmitField('Αποθήκευση')

class RevenueForm(FlaskForm):
    date = DateField('Ημερομηνία', format='%Y-%m-%d', validators=[DataRequired()])
    amount = FloatField('Ποσό (€)', validators=[DataRequired()])
    category = StringField('Κατηγορία', validators=[DataRequired()])
    store_id = SelectField('Κατάστημα', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Καταχώριση')

class ExpenseForm(FlaskForm):
    date = DateField('Ημερομηνία', format='%Y-%m-%d', validators=[DataRequired()])
    amount = FloatField('Ποσό (€)', validators=[DataRequired()])
    store_id = SelectField('Κατάστημα', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Καταχώριση')


class InventoryForm(FlaskForm):
    name = StringField('Όνομα Προϊόντος', validators=[DataRequired()])
    code = StringField('Κωδικός', validators=[Optional()])
    quantity = FloatField('Ποσότητα', validators=[DataRequired()])
    unit = StringField('Μονάδα Μέτρησης (π.χ. κιλά, τεμ)', validators=[DataRequired()])
    min_quantity = FloatField('Ελάχιστη Ποσότητα (προειδοποίηση)', validators=[Optional()])
    store_id = SelectField('Κατάστημα', coerce=int, validators=[DataRequired()])

    submit = SubmitField('Αποθήκευση')    

class PayrollForm(FlaskForm):
    personnel_id = SelectField('Εργαζόμενος', coerce=int, validators=[DataRequired()])
    store_id = SelectField('Κατάστημα', coerce=int, validators=[DataRequired()])
    date = DateField('Ημερομηνία', format='%Y-%m-%d', validators=[DataRequired()])
    gross_amount = FloatField('Μικτές Αποδοχές (€)', validators=[DataRequired()])
    net_amount = FloatField('Καθαρές Αποδοχές (€)', validators=[DataRequired()])
    bonus = FloatField('Bonus (€)', validators=[Optional()])
    payment_method = SelectField('Τρόπος Πληρωμής', choices=[
        ('Μετρητά', 'Μετρητά'),
        ('Κατάθεση', 'Κατάθεση'),
        ('Άλλο', 'Άλλο')
    ], validators=[DataRequired()])
    submit = SubmitField('Αποθήκευση')

    def __init__(self, *args, **kwargs):
        super(PayrollForm, self).__init__(*args, **kwargs)
        self.store_id.choices = [(s.id, s.name) for s in Store.query.all()]
        self.personnel_id.choices = [(p.id, f"{p.first_name} {p.last_name}") for p in Personnel.query.all()]    