from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, DateField, SelectField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired
from app.models import Store, Client

class InvoiceLineForm(FlaskForm):
    product_name = StringField('Προϊόν', validators=[DataRequired()])
    quantity = FloatField('Ποσότητα', validators=[DataRequired()])
    unit_price = FloatField('Τιμή Μονάδας (€)', validators=[DataRequired()])

class InvoiceForm(FlaskForm):
    date = DateField('Ημερομηνία', format='%Y-%m-%d', validators=[DataRequired()])
    client_id = SelectField('Πελάτης', coerce=int, validators=[DataRequired()])
    store_id = SelectField('Κατάστημα', coerce=int, validators=[DataRequired()])
    lines = FieldList(FormField(InvoiceLineForm), min_entries=1)
    submit = SubmitField('Καταχώριση')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id.choices = [(c.id, c.name) for c in Client.query.order_by(Client.name).all()]
        self.store_id.choices = [(s.id, s.name) for s in Store.query.order_by(Store.name).all()]