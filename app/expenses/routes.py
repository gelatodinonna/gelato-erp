# app/expenses/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.extensions import db
from app.models import Expense, Store
from app.expenses.forms import ExpenseForm
from app.forms import DeleteForm
from sqlalchemy import and_

expenses_bp = Blueprint('expenses', __name__, url_prefix='/expenses')

@expenses_bp.route('/')
def index():
    stores = Store.query.all()
    selected_store = request.args.get('store', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Expense.query

    if selected_store:
        query = query.filter(Expense.store_id == selected_store)
    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)

    expenses = query.order_by(Expense.date.desc()).all()

    return render_template(
        'expenses/index.html',
        expenses=expenses,
        stores=stores,
        selected_store=selected_store,
        start_date=start_date,
        end_date=end_date,
        delete_form=DeleteForm()
    )

@expenses_bp.route('/add', methods=['GET', 'POST'])
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(
            date=form.date.data,
            amount=form.amount.data,
            store_id=form.store_id.data
        )
        db.session.add(expense)
        db.session.commit()
        flash("Το έξοδο καταχωρήθηκε!", "success")
        return redirect(url_for('expenses.index'))
    return render_template('expenses/add.html', form=form)

@expenses_bp.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    form = ExpenseForm(obj=expense)
    if form.validate_on_submit():
        expense.date = form.date.data
        expense.amount = form.amount.data
        expense.store_id = form.store_id.data
        db.session.commit()
        flash("Το έξοδο ενημερώθηκε!", "success")
        return redirect(url_for('expenses.index'))
    return render_template('expenses/edit.html', form=form, expense=expense)

@expenses_bp.route('/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    flash("Το έξοδο διαγράφηκε.", "info")
    return redirect(url_for('expenses.index'))