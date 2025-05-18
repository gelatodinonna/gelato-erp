# app/revenues/forms.py
from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired
from app.models import Store

class RevenueForm(FlaskForm):
    date = DateField('Ημερομηνία', validators=[DataRequired()], format='%Y-%m-%d')
    amount = FloatField('Ποσό (€)', validators=[DataRequired()])
    category = StringField('Κατηγορία', validators=[DataRequired()])
    store_id = SelectField('Κατάστημα', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Αποθήκευση')

    def __init__(self, *args, **kwargs):
        super(RevenueForm, self).__init__(*args, **kwargs)
        from app.models import Store
        self.store_id.choices = [(store.id, store.name) for store in Store.query.order_by(Store.name).all()]