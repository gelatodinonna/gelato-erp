from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models.inventory import InventoryItem
from app.models.store import Store
from app.extensions import db
from app.forms.inventory import InventoryForm

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory_bp.route('/')
def index():
    store_id = request.args.get('store_id', type=int)
    query = InventoryItem.query

    if store_id:
        query = query.filter_by(store_id=store_id)

    items = query.order_by(InventoryItem.name).all()
    stores = Store.query.all()

    return render_template('inventory/index.html', items=items, stores=stores, selected_store=store_id)

@inventory_bp.route('/new', methods=['GET', 'POST'])
def new_item():
    form = InventoryForm()
    form.store_id.choices = [(s.id, s.name) for s in Store.query.all()]

    if form.validate_on_submit():
        item = InventoryItem(
            name=form.name.data,
            code=form.code.data,
            quantity=form.quantity.data,
            unit=form.unit.data,
            min_quantity=form.min_quantity.data,
            store_id=form.store_id.data
        )
        db.session.add(item)
        db.session.commit()
        flash('Το προϊόν προστέθηκε στην αποθήκη!', 'success')
        return redirect(url_for('inventory.index'))

    return render_template('inventory/new.html', form=form)

@inventory_bp.route('/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_item(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    form = InventoryForm(obj=item)
    form.store_id.choices = [(s.id, s.name) for s in Store.query.all()]

    if form.validate_on_submit():
        item.name = form.name.data
        item.code = form.code.data
        item.quantity = form.quantity.data
        item.unit = form.unit.data
        item.min_quantity = form.min_quantity.data
        item.store_id = form.store_id.data
        db.session.commit()
        flash('Το προϊόν ενημερώθηκε.', 'success')
        return redirect(url_for('inventory.index'))

    return render_template('inventory/edit.html', form=form, item=item)

@inventory_bp.route('/<int:item_id>/delete', methods=['POST'])
def delete_item(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Το προϊόν διαγράφηκε από την αποθήκη.', 'warning')
    return redirect(url_for('inventory.index'))