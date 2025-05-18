from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired

class MaterialForm(FlaskForm):
    name = StringField('Όνομα Υλικού', validators=[DataRequired()])
    quantity = FloatField('Ποσότητα', validators=[DataRequired()])
    unit = StringField('Μονάδα (π.χ. κιλά, λίτρα, τμχ)', validators=[DataRequired()])
    cost = FloatField('Κόστος ανά μονάδα', validators=[DataRequired()])
    store_id = SelectField('Κατάστημα', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Αποθήκευση')