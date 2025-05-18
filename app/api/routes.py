from flask import Blueprint, jsonify
from app.models import Employee

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/employees/<int:store_id>')
def get_employees_by_store(store_id):
    employees = Employee.query.filter_by(store_id=store_id, active=True).order_by(Employee.last_name).all()
    result = [
        {'id': e.id, 'name': f"{e.first_name} {e.last_name}"}
        for e in employees
    ]
    return jsonify(result)