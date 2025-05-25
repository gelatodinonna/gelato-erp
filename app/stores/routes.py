from flask import Blueprint, render_template, redirect, url_for, flash, request
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models import Store
from app.stores.forms import StoreForm

stores_bp = Blueprint('stores', __name__, url_prefix='/stores')

@stores_bp.route('/')
def index():
    stores = Store.query.order_by(Store.name).all()
    return render_template('stores/index.html', stores=stores)

@stores_bp.route('/add', methods=['GET', 'POST'])
def add_store():
    form = StoreForm()
    if form.validate_on_submit():
        new_store = Store(
            name=form.name.data,
            location=form.location.data,
            vat_number=form.vat_number.data,
            phone=form.phone.data,
            address=form.address.data
        )
        db.session.add(new_store)
        db.session.commit()
        flash('Το κατάστημα προστέθηκε επιτυχώς!', 'success')
        return redirect(url_for('stores.index'))
    return render_template('stores/add.html', form=form)

@stores_bp.route('/edit/<int:store_id>', methods=['GET', 'POST'])
def edit_store(store_id):
    store = Store.query.get_or_404(store_id)
    form = StoreForm(obj=store)
    if form.validate_on_submit():
        store.name = form.name.data
        store.location = form.location.data
        store.vat_number = form.vat_number.data
        store.phone = form.phone.data
        store.address = form.address.data  
        db.session.commit()
        flash('Το κατάστημα ενημερώθηκε επιτυχώς!', 'success')
        return redirect(url_for('stores.index'))
    return render_template('stores/edit.html', form=form, store=store)

@stores_bp.route('/delete/<int:store_id>', methods=['POST'])
def delete_store(store_id):
    store = Store.query.get_or_404(store_id)
    try:
        db.session.delete(store)
        db.session.commit()
        flash('Το κατάστημα διαγράφηκε επιτυχώς.', 'info')
    except IntegrityError:
        db.session.rollback()
        flash('Δεν είναι δυνατή η διαγραφή. Υπάρχουν συνδεδεμένα δεδομένα με το κατάστημα (π.χ. προσωπικό, έξοδα, έσοδα).', 'danger')
    return redirect(url_for('stores.index'))