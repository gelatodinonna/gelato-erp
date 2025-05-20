from flask_wtf import FlaskForm
from wtforms import FloatField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional
from app.models import Store

class ExpenseForm(FlaskForm):
    date = DateField('Ημερομηνία', format='%Y-%m-%d', validators=[DataRequired()])
    amount = FloatField('Ποσό (€)', validators=[DataRequired()])
    description = TextAreaField('Περιγραφή', validators=[Optional()])
    store_id = SelectField('Κατάστημα', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Αποθήκευση')

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.store_id.choices = [(store.id, store.name) for store in Store.query.order_by(Store.name).all()]