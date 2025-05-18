from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import Revenue, Expense, Store, Employee
from app.forms import RevenueForm, ExpenseForm, StoreForm
from app.extensions import db
from datetime import datetime
from app.forms.payroll import PayrollForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():
    stores_count = Store.query.count()
    employee_count = Employee.query.count()
    sales_total = db.session.query(db.func.sum(Revenue.amount)).scalar() or 0

    recent_revenues = Revenue.query.order_by(Revenue.date.desc()).limit(5).all()
    recent_expenses = Expense.query.order_by(Expense.date.desc()).limit(5).all()

    return render_template(
        'main/dashboard.html',
        stores_count=stores_count,
        employee_count=employee_count,
        sales_total=sales_total,
        recent_revenues=recent_revenues,
        recent_expenses=recent_expenses
    )

# Revenue
@main_bp.route('/revenues/new', methods=['GET', 'POST'])
def new_revenue():
    form = RevenueForm()
    form.store_id.choices = [(s.id, s.name) for s in Store.query.all()]
    if form.validate_on_submit():
        revenue = Revenue(
            date=form.date.data,
            amount=form.amount.data,
            category=form.category.data,
            store_id=form.store_id.data
        )
        db.session.add(revenue)
        db.session.commit()
        flash('Το έσοδο καταχωρήθηκε.', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('revenues/new.html', form=form)

# Expense
@main_bp.route('/expenses/new', methods=['GET', 'POST'])
def new_expense():
    form = ExpenseForm()
    form.store_id.choices = [(s.id, s.name) for s in Store.query.all()]
    if form.validate_on_submit():
        expense = Expense(
            date=form.date.data,
            amount=form.amount.data,
            store_id=form.store_id.data
        )
        db.session.add(expense)
        db.session.commit()
        flash('Το έξοδο καταχωρήθηκε.', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('expenses/new.html', form=form)

# Store
@main_bp.route('/stores/new', methods=['GET', 'POST'])
def new_store():
    form = StoreForm()
    if form.validate_on_submit():
        store = Store(name=form.name.data, location=form.location.data)
        db.session.add(store)
        db.session.commit()
        flash('Το κατάστημα προστέθηκε.', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('stores/new.html', form=form)

payroll_bp = Blueprint('payroll', __name__, url_prefix='/payroll')

@payroll_bp.route('/')
def payroll_home():
    payrolls = Payroll.query.order_by(Payroll.date.desc()).all()
    return render_template('payroll/index.html', payrolls=payrolls)

@payroll_bp.route('/new', methods=['GET', 'POST'])
def new_payroll():
    form = PayrollForm()
    if form.validate_on_submit():
        payroll = Payroll(
            personnel_id=form.personnel_id.data,
            store_id=form.store_id.data,
            date=form.date.data,
            gross_amount=form.gross_amount.data,
            net_amount=form.net_amount.data,
            bonus=form.bonus.data,
            payment_method=form.payment_method.data
        )
        db.session.add(payroll)
        db.session.commit()
        flash('Η μισθοδοσία καταχωρήθηκε επιτυχώς!', 'success')
        return redirect(url_for('payroll.payroll_home'))
    return render_template('payroll/new.html', form=form)

@payroll_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_payroll(id):
    payroll = Payroll.query.get_or_404(id)
    form = PayrollForm(obj=payroll)
    if form.validate_on_submit():
        payroll.personnel_id = form.personnel_id.data
        payroll.store_id = form.store_id.data
        payroll.date = form.date.data
        payroll.gross_amount = form.gross_amount.data
        payroll.net_amount = form.net_amount.data
        payroll.bonus = form.bonus.data
        payroll.payment_method = form.payment_method.data
        db.session.commit()
        flash('Η μισθοδοσία ενημερώθηκε!', 'success')
        return redirect(url_for('payroll.payroll_home'))
    return render_template('payroll/edit.html', form=form, payroll=payroll)

@payroll_bp.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_payroll(id):
    payroll = Payroll.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(payroll)
        db.session.commit()
        flash('Η εγγραφή διαγράφηκε.', 'warning')
        return redirect(url_for('payroll.payroll_home'))
    return render_template('payroll/delete.html', payroll=payroll)