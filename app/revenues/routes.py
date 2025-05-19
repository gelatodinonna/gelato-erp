# app/revenues/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.extensions import db
from app.models import Revenue, Store
from app.revenues.forms import RevenueForm
from sqlalchemy import and_
from app.forms import DeleteForm

revenues_bp = Blueprint('revenues', __name__, url_prefix='/revenues')

@revenues_bp.route('/', methods=['GET'])
def index():
    stores = Store.query.all()
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
        'revenues/index.html',
        revenues=revenues,
        stores=stores,
        selected_store=selected_store,
        start_date=start_date,
        end_date=end_date,
        delete_form=DeleteForm()
    )

@revenues_bp.route('/add', methods=['GET', 'POST'])
def add_revenue():
    form = RevenueForm()
    if form.validate_on_submit():
        new_revenue = Revenue(
            date=form.date.data,
            amount=form.amount.data,
            category=form.category.data,
            store_id=form.store_id.data
        )
        db.session.add(new_revenue)
        db.session.commit()
        flash("Το έσοδο καταχωρήθηκε!", "success")
        return redirect(url_for('revenues.index'))
    return render_template('revenues/add.html', form=form)

@revenues_bp.route('/edit/<int:revenue_id>', methods=['GET', 'POST'])
def edit_revenue(revenue_id):
    revenue = Revenue.query.get_or_404(revenue_id)
    form = RevenueForm(obj=revenue)
    if form.validate_on_submit():
        revenue.date = form.date.data
        revenue.amount = form.amount.data
        revenue.category = form.category.data
        revenue.store_id = form.store_id.data
        db.session.commit()
        flash("Το έσοδο ενημερώθηκε!", "success")
        return redirect(url_for('revenues.index'))
    return render_template('revenues/edit.html', form=form, revenue=revenue)

@revenues_bp.route('/delete/<int:revenue_id>', methods=['POST'])
def delete_revenue(revenue_id):
    form = DeleteForm()
    if form.validate_on_submit():
        revenue = Revenue.query.get_or_404(revenue_id)
        db.session.delete(revenue)
        db.session.commit()
        flash("Το έσοδο διαγράφηκε.", "success")
    else:
        flash("Αποτυχία διαγραφής: CSRF token λείπει ή μη έγκυρο.", "danger")
    return redirect(url_for('revenues.view_revenues'))