# app/payroll/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.extensions import db
from app.models import Payroll, Store, Employee
from app.payroll.forms import PayrollForm
from sqlalchemy import extract

payroll_bp = Blueprint('payroll', __name__, url_prefix='/payroll')

# Προβολή όλων των μισθοδοσιών με φίλτρα
@payroll_bp.route('/')
def index():
    stores = Store.query.all()
    selected_store = request.args.get('store', type=int)
    selected_month = request.args.get('month', type=int)
    selected_year = request.args.get('year', type=int)

    query = Payroll.query

    if selected_store:
        query = query.filter(Payroll.store_id == selected_store)
    if selected_month:
        query = query.filter(extract('month', Payroll.date) == selected_month)
    if selected_year:
        query = query.filter(extract('year', Payroll.date) == selected_year)

    payrolls = query.order_by(Payroll.date.desc()).all()

    return render_template(
        'payroll/index.html',
        payrolls=payrolls,
        stores=stores,
        selected_store=selected_store,
        selected_month=selected_month,
        selected_year=selected_year
    )

@payroll_bp.route('/add', methods=['GET', 'POST'])
def add_payroll():
    # Πρώτο κατάστημα για GET
    first_store = Store.query.order_by(Store.name).first()
    store_id = request.form.get('store_id', type=int) or (first_store.id if first_store else None)
    
    form = PayrollForm(store_id=store_id)

    if form.validate_on_submit():
        payroll = Payroll(
            date=form.date.data,
            gross_amount=form.gross_amount.data,
            net_amount=form.net_amount.data,
            bonus=form.bonus.data,
            payment_method=form.payment_method.data,
            store_id=form.store_id.data,
            employee_id=form.employee_id.data
        )
        db.session.add(payroll)
        db.session.commit()
        flash("Η μισθοδοσία καταχωρήθηκε!", "success")
        return redirect(url_for('payroll.index'))

    return render_template('payroll/add.html', form=form)

# Επεξεργασία υπάρχουσας μισθοδοσίας
@payroll_bp.route('/edit/<int:payroll_id>', methods=['GET', 'POST'])
def edit_payroll(payroll_id):
    payroll = Payroll.query.get_or_404(payroll_id)
    form = PayrollForm(store_id=payroll.store_id, obj=payroll)

    if form.validate_on_submit():
        payroll.date = form.date.data
        payroll.gross_amount = form.gross_amount.data
        payroll.net_amount = form.net_amount.data
        payroll.bonus = form.bonus.data
        payroll.payment_method = form.payment_method.data
        payroll.store_id = form.store_id.data
        payroll.employee_id = form.employee_id.data
        db.session.commit()
        flash("Η μισθοδοσία ενημερώθηκε!", "success")
        return redirect(url_for('payroll.index'))

    return render_template('payroll/edit.html', form=form, payroll=payroll)

# Διαγραφή μισθοδοσίας
@payroll_bp.route('/delete/<int:payroll_id>', methods=['POST'])
def delete_payroll(payroll_id):
    payroll = Payroll.query.get_or_404(payroll_id)
    db.session.delete(payroll)
    db.session.commit()
    flash("Η μισθοδοσία διαγράφηκε.", "info")
    return redirect(url_for('payroll.index'))