# app/models.py ή app/payroll/models.py

from app.extensions import db
from datetime import datetime

class Payroll(db.Model):
    __tablename__ = 'payroll'
    id = db.Column(db.Integer, primary_key=True)
    personnel_id = db.Column(db.Integer, db.ForeignKey('personnel.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    gross_amount = db.Column(db.Float, nullable=False)
    net_amount = db.Column(db.Float, nullable=False)
    bonus = db.Column(db.Float, nullable=True)
    payment_method = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.String(255), nullable=True)

    personnel = db.relationship('Personnel', backref='payrolls')