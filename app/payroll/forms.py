from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional
from app.models import Store, Employee

class PayrollForm(FlaskForm):
    date = DateField('Ημερομηνία', format='%Y-%m-%d', validators=[DataRequired()])
    gross_amount = FloatField('Μικτά (€)', validators=[DataRequired()])
    net_amount = FloatField('Καθαρά (€)', validators=[DataRequired()])
    bonus = FloatField('Bonus (€)', validators=[Optional()])
    
    payment_method = SelectField(
        'Τρόπος Πληρωμής',
        choices=[
            ('Μετρητά', 'Μετρητά'),
            ('Τραπεζική Κατάθεση', 'Τραπεζική Κατάθεση')
        ],
        validators=[DataRequired()]
    )
    
    store_id = SelectField('Κατάστημα', coerce=int, validators=[DataRequired()])
    employee_id = SelectField('Εργαζόμενος', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Αποθήκευση')

    def __init__(self, store_id=None, *args, **kwargs):
        super(PayrollForm, self).__init__(*args, **kwargs)
        
        self.store_id.choices = [
            (s.id, s.name) for s in Store.query.order_by(Store.name).all()
        ]

        if store_id:
            self.employee_id.choices = [
                (e.id, f"{e.first_name} {e.last_name}")
                for e in Employee.query.filter_by(store_id=store_id, active=True).order_by(Employee.last_name)
            ]
        else:
            self.employee_id.choices = []