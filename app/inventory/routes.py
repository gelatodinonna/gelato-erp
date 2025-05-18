from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import Material, Store
from app.inventory.forms import MaterialForm
from app.extensions import db

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory_bp.route('/')
def list_materials():
    materials = Material.query.all()
    return render_template('inventory/list.html', materials=materials)

@inventory_bp.route('/new', methods=['GET', 'POST'])
def add_material():
    form = MaterialForm()
    form.store_id.choices = [(store.id, store.name) for store in Store.query.all()]
    if form.validate_on_submit():
        material = Material(
            name=form.name.data,
            quantity=form.quantity.data,
            unit=form.unit.data,
            cost=form.cost.data,
            store_id=form.store_id.data
        )
        db.session.add(material)
        db.session.commit()
        flash('Το υλικό προστέθηκε!', 'success')
        return redirect(url_for('inventory.list_materials'))
    return render_template('inventory/new.html', form=form)

@inventory_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_material(id):
    material = Material.query.get_or_404(id)
    form = MaterialForm(obj=material)
    form.store_id.choices = [(store.id, store.name) for store in Store.query.all()]
    if form.validate_on_submit():
        material.name = form.name.data
        material.quantity = form.quantity.data
        material.unit = form.unit.data
        material.cost = form.cost.data
        material.store_id = form.store_id.data
        db.session.commit()
        flash('Το υλικό ενημερώθηκε!', 'success')
        return redirect(url_for('inventory.list_materials'))
    return render_template('inventory/edit.html', form=form, material=material)

@inventory_bp.route('/delete/<int:id>', methods=['POST'])
def delete_material(id):
    material = Material.query.get_or_404(id)
    db.session.delete(material)
    db.session.commit()
    flash('Το υλικό διαγράφηκε.', 'warning')
    return redirect(url_for('inventory.list_materials'))