from app.extensions import db
from datetime import datetime

class Personnel(db.Model):
    __tablename__ = 'personnel'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    father_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    vat = db.Column(db.String(20))
    amka = db.Column(db.String(11))
    telephone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    iban = db.Column(db.String(34))
    ama = db.Column(db.String(20))
    hire_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)