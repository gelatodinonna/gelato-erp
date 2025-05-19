from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import Employee, Store  # Προσοχή: Χρησιμοποιούμε το Employee ως κεντρικό μοντέλο
from app.hr.forms import EmployeeForm  # Το σωστό όνομα της φόρμας
from app.extensions import db

hr_bp = Blueprint('hr', __name__, url_prefix='/hr')


# Λίστα εργαζομένων
@hr_bp.route('/')
def list_personnel():
    employees = Employee.query.order_by(Employee.last_name).all()
    return render_template('hr/list.html', personnel=employees)


# Δημιουργία νέου εργαζομένου
@hr_bp.route('/new', methods=['GET', 'POST'])
def add_personnel():
    form = EmployeeForm()
    form.store_id.choices = [(s.id, s.name) for s in Store.query.order_by(Store.name).all()]

    if form.validate_on_submit():
        new_employee = Employee(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            father_name=form.father_name.data,
            age=form.age.data,
            vat=form.vat.data,
            amka=form.amka.data,
            phone=form.phone.data,
            address=form.address.data,
            iban=form.iban.data,
            ama=form.ama.data,
            store_id=form.store_id.data
        )
        db.session.add(new_employee)
        db.session.commit()
        flash('Ο εργαζόμενος καταχωρήθηκε!', 'success')
        return redirect(url_for('hr.list_personnel'))

    return render_template('hr/new.html', form=form)


# Επεξεργασία εργαζομένου
@hr_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_personnel(id):
    employee = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=employee)
    form.store_id.choices = [(s.id, s.name) for s in Store.query.order_by(Store.name).all()]

    if form.validate_on_submit():
        employee.first_name = form.first_name.data
        employee.last_name = form.last_name.data
        employee.father_name = form.father_name.data
        employee.age = form.age.data
        employee.vat = form.vat.data
        employee.amka = form.amka.data
        employee.phone = form.phone.data
        employee.address = form.address.data
        employee.iban = form.iban.data
        employee.ama = form.ama.data
        employee.store_id = form.store_id.data

        db.session.commit()
        flash('Τα στοιχεία ενημερώθηκαν!', 'success')
        return redirect(url_for('hr.list_personnel'))

    return render_template('hr/edit.html', form=form, person=employee)


# Διαγραφή εργαζομένου
@hr_bp.route('/delete/<int:employee_id>', methods=['POST'])
def delete_personnel(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    flash('Ο υπάλληλος διαγράφηκε με επιτυχία.', 'success')
    return redirect(url_for('hr.list_personnel'))