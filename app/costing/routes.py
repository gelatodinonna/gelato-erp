from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.extensions import db
from app.models import Product, ProductCosting, Store, Material
from app.costing.forms import ProductCostingForm

costing_bp = Blueprint('costing', __name__, url_prefix='/costing')

@costing_bp.route('/')
def index():
    costings = ProductCosting.query.order_by(ProductCosting.product_id).all()
    return render_template('costing/index.html', costings=costings)

@costing_bp.route('/add', methods=['GET', 'POST'])
def add_costing():
    stores = Store.query.order_by(Store.name).all()
    form = ProductCostingForm()

    if form.validate_on_submit():
        # Δημιουργία προϊόντος αν δεν υπάρχει
        product = Product.query.filter_by(name=form.product_name.data).first()
        if not product:
            product = Product(name=form.product_name.data)
            db.session.add(product)
            db.session.flush()  # για να πάρει ID

        costing = ProductCosting(
            product_id=product.id,
            material_id=form.material_id.data,
            quantity=form.quantity.data,
            unit_yield=form.unit_yield.data or 1.0
        )
        db.session.add(costing)
        db.session.commit()
        flash("Η κοστολόγηση προστέθηκε!", "success")
        return redirect(url_for('costing.index'))

    return render_template('costing/costing.html', form=form, stores=stores)

@costing_bp.route('/edit/<int:costing_id>', methods=['GET', 'POST'])
def edit_costing(costing_id):
    costing = ProductCosting.query.get_or_404(costing_id)
    form = ProductCostingForm(obj=costing)
    stores = Store.query.order_by(Store.name).all()

    # Προκαθορισμένο store για σωστή φόρτωση υλικών
    form.material_id.choices = [
        (m.id, f"{m.name} ({m.unit})") for m in
        Material.query.filter_by(store_id=costing.material.store_id).order_by(Material.name)
    ]

    if form.validate_on_submit():
        costing.product.name = form.product_name.data
        costing.material_id = form.material_id.data
        costing.quantity = form.quantity.data
        costing.unit_yield = form.unit_yield.data or 1.0
        db.session.commit()
        flash("Η κοστολόγηση ενημερώθηκε!", "success")
        return redirect(url_for('costing.index'))

    # Προκαθορισμένο όνομα προϊόντος
    form.product_name.data = costing.product.name
    return render_template('costing/edit.html', form=form, stores=stores)  

@costing_bp.route('/delete/<int:costing_id>', methods=['POST'])
def delete_costing(costing_id):
    costing = ProductCosting.query.get_or_404(costing_id)
    db.session.delete(costing)
    db.session.commit()
    flash("Η κοστολόγηση διαγράφηκε!", "info")
    return redirect(url_for('costing.index'))      