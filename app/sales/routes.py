from flask import Blueprint, render_template, request
from app.models import Revenue, Store
from sqlalchemy import and_
from app.extensions import db

sales_bp = Blueprint('sales', __name__, url_prefix='/sales')

@sales_bp.route('/')
def index():
    stores = Store.query.order_by(Store.name).all()
    selected_store = request.args.get('store', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Revenue.query

    if selected_store:
        query = query.filter(Revenue.store_id == selected_store)
    if start_date:
        query = query.filter(Revenue.date >= start_date)
    if end_date:
        query = query.filter(Revenue.date <= end_date)

    revenues = query.order_by(Revenue.date.desc()).all()

    return render_template(
        'sales/index.html',
        revenues=revenues,
        stores=stores,
        selected_store=selected_store,
        start_date=start_date,
        end_date=end_date
    )