from flask import Blueprint, render_template
from app.extensions import db
from app.models import Store, Employee, Revenue

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():
    stores_count = Store.query.count()
    employee_count = Employee.query.count()
    # Άθροισμα πωλήσεων (εσόδων)
    sales_total = db.session.query(db.func.sum(Revenue.amount)).scalar() or 0
    return render_template(
        'main/dashboard.html',
        stores_count=stores_count,
        employee_count=employee_count,
        sales_total=sales_total
    )