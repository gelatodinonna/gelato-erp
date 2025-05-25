from flask import Blueprint, render_template
from app.extensions import db
from app.models import Store, Employee, Revenue, Expense
from sqlalchemy import func
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():
    stores = Store.query.all()
    stores_count = len(stores)
    personnel_count = Employee.query.count()
    sales_total = db.session.query(func.sum(Revenue.amount)).scalar() or 0

    current_year = datetime.now().year

    balances_by_store = {}
    for store in stores:
        monthly_balances = {}
        for month in range(1, 13):
            revenue = db.session.query(func.sum(Revenue.amount)).filter(
                Revenue.store_id == store.id,
                func.strftime('%m', Revenue.date) == f"{month:02}",
                func.strftime('%Y', Revenue.date) == str(current_year)
            ).scalar() or 0

            expense = db.session.query(func.sum(Expense.amount)).filter(
                Expense.store_id == store.id,
                func.strftime('%m', Expense.date) == f"{month:02}",
                func.strftime('%Y', Expense.date) == str(current_year)
            ).scalar() or 0

            monthly_balances[month] = revenue - expense

        balances_by_store[store.name] = monthly_balances

    return render_template(
        'main/dashboard.html',
        stores_count=stores_count,
        personnel_count=personnel_count,
        sales_total=sales_total,
        balances_by_store=balances_by_store,
        current_year=current_year
    )