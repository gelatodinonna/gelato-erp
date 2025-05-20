from datetime import datetime
from app.extensions import db

class Store(db.Model):
    __tablename__ = 'store'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=True)
    inventory_items = db.relationship('InventoryItem', back_populates='store')
    revenues = db.relationship('Revenue', back_populates='store')
    expenses = db.relationship('Expense', back_populates='store')
    payrolls = db.relationship('Payroll', back_populates='store')
    materials = db.relationship('Material', back_populates='store')
    invoices = db.relationship('Invoice', back_populates='store')
    employees = db.relationship('Employee', back_populates='store')

    def __repr__(self):
        return f"<Store {self.name}>"

class Revenue(db.Model):
    __tablename__ = 'revenue'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    store = db.relationship('Store', back_populates='revenues')

class Expense(db.Model):
    __tablename__ = 'expense'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    store = db.relationship('Store', back_populates='expenses')

class InventoryItem(db.Model):
    __tablename__ = 'inventory_item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    min_quantity = db.Column(db.Float, default=0.0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    store = db.relationship('Store', back_populates='inventory_items')

    def __repr__(self):
        return f"<InventoryItem {self.name} - {self.store.name}>"

class Payroll(db.Model):
    __tablename__ = 'payroll'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    gross_amount = db.Column(db.Float, nullable=False)
    net_amount = db.Column(db.Float, nullable=False)
    bonus = db.Column(db.Float, nullable=True)
    payment_method = db.Column(db.String(20), nullable=False)

    store = db.relationship('Store', back_populates='payrolls')
    employee = db.relationship('Employee', back_populates='payrolls')

class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    father_name = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    vat = db.Column(db.String(15), nullable=True)
    amka = db.Column(db.String(15), nullable=True)
    telephone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    iban = db.Column(db.String(34), nullable=True)
    ama = db.Column(db.String(20), nullable=True)
    position = db.Column(db.String(50), nullable=True)
    hire_date = db.Column(db.Date, nullable=True)
    active = db.Column(db.Boolean, default=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)

    store = db.relationship('Store', back_populates='employees')
    payrolls = db.relationship('Payroll', back_populates='employee', cascade='all, delete-orphan')

class Material(db.Model):
    __tablename__ = 'material'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=0.0)
    unit = db.Column(db.String(20), nullable=False)
    cost = db.Column(db.Float, nullable=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)

    store = db.relationship('Store', back_populates='materials')

    def __repr__(self):
        return f"<Material {self.name}>"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class ProductCosting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit_yield = db.Column(db.Float, nullable=True)

    product = db.relationship('Product', backref='costings')
    material = db.relationship('Material')

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), unique=True, nullable=True)
    date = db.Column(db.Date, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)

    client = db.relationship('Client', backref='invoices')
    store = db.relationship('Store', back_populates='invoices')
    lines = db.relationship("InvoiceLine", backref="invoice", lazy=True)

    @property
    def total_amount(self):
        return sum(line.quantity * line.unit_price for line in self.lines)

class InvoiceLine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)

    @property
    def line_total(self):
        return self.quantity * self.unit_price

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(256))
    phone = db.Column(db.String(20))
    vat_number = db.Column(db.String(20))
    email = db.Column(db.String(120))