from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional
from app.models import Store

class ProductCostingForm(FlaskForm):
    product_name = StringField('Προϊόν', validators=[DataRequired()])
    store_id = SelectField('Κατάστημα', coerce=int, validators=[DataRequired()])
    material_id = SelectField('Υλικό', coerce=int, validators=[DataRequired()])
    quantity = FloatField('Ποσότητα Υλικού', validators=[DataRequired()])
    unit_yield = FloatField('Απόδοση (σε μονάδες προϊόντος)', validators=[Optional()])
    submit = SubmitField('Καταχώριση')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.store_id.choices = [(s.id, s.name) for s in Store.query.order_by(Store.name)]
        self.material_id.choices = []  # γεμίζει δυναμικά με JS