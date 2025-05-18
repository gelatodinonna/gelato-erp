# app/reports/routes.py
from flask import Blueprint, render_template
from app.extensions import db
from app.models import Revenue, Expense, Store
from sqlalchemy import extract, func

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

@reports_bp.route('/')
def index():
    # Έσοδα ανά μήνα & κατάστημα
    revenue_data = db.session.query(
        extract('year', Revenue.date).label('year'),
        extract('month', Revenue.date).label('month'),
        Store.name.label('store_name'),
        func.sum(Revenue.amount).label('total_revenue')
    ).join(Store).group_by('year', 'month', 'store_name').all()

    # Έξοδα ανά μήνα & κατάστημα
    expense_data = db.session.query(
        extract('year', Expense.date).label('year'),
        extract('month', Expense.date).label('month'),
        Store.name.label('store_name'),
        func.sum(Expense.amount).label('total_expense')
    ).join(Store).group_by('year', 'month', 'store_name').all()

    # Συγχώνευση αποτελεσμάτων
    report = {}

    for row in revenue_data:
        key = (int(row.year), int(row.month), row.store_name)
        report[key] = {
            'year': row.year,
            'month': row.month,
            'store_name': row.store_name,
            'total_revenue': float(row.total_revenue),
            'total_expense': 0,
        }

    for row in expense_data:
        key = (int(row.year), int(row.month), row.store_name)
        if key in report:
            report[key]['total_expense'] = float(row.total_expense)
        else:
            report[key] = {
                'year': row.year,
                'month': row.month,
                'store_name': row.store_name,
                'total_revenue': 0,
                'total_expense': float(row.total_expense),
            }

    # Ταξινόμηση ανά έτος, μήνα, κατάστημα
    sorted_report = sorted(report.values(), key=lambda x: (x['year'], x['month'], x['store_name']))

    return render_template('reports/index.html', report_data=sorted_report)