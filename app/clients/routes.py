# app/clients/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.extensions import db
from app.models import Client
from app.clients.forms import ClientForm

clients_bp = Blueprint('clients', __name__, url_prefix='/clients')

@clients_bp.route('/')
def index():
    clients = Client.query.order_by(Client.name.asc()).all()
    return render_template('clients/index.html', clients=clients)

@clients_bp.route('/add', methods=['GET', 'POST'])
def add_client():
    form = ClientForm()
    if form.validate_on_submit():
        new_client = Client(
            name=form.name.data,
            vat_number=form.vat_number.data,
            address=form.address.data,
            phone=form.phone.data,
            email=form.email.data
        )
        db.session.add(new_client)
        db.session.commit()
        flash("Ο πελάτης προστέθηκε επιτυχώς!", "success")
        return redirect(url_for('clients.index'))
    return render_template('clients/add.html', form=form)    

@clients_bp.route('/<int:client_id>/delete', methods=['POST'], endpoint='delete_client')
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash('Ο πελάτης διαγράφηκε επιτυχώς.', 'success')
    return redirect(url_for('clients.index'))    

@clients_bp.route('/<int:client_id>')
def view_client(client_id):
    client = Client.query.get_or_404(client_id)
    return render_template('clients/view.html', client=client)

@clients_bp.route('/<int:client_id>/edit', methods=['GET', 'POST'])
def edit_client(client_id):
    client = Client.query.get_or_404(client_id)
    form = ClientForm(obj=client)

    if form.validate_on_submit():
        form.populate_obj(client)
        db.session.commit()
        flash("Ο πελάτης ενημερώθηκε.", "success")
        return redirect(url_for('clients.index'))

    return render_template('clients/edit.html', form=form)    