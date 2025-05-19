from flask import Blueprint, render_template, redirect, url_for, flash, request, make_response
from app.extensions import db
from app.models import Invoice, InvoiceLine, Client, Store
from app.invoices.forms import InvoiceForm
from sqlalchemy.orm import joinedload

from weasyprint import HTML
import qrcode
import io
import base64

invoices_bp = Blueprint('invoices', __name__, url_prefix='/invoices')

# Προβολή όλων των τιμολογίων
@invoices_bp.route('/')
def invoice_list():
    invoices = Invoice.query.options(
        joinedload(Invoice.client),
        joinedload(Invoice.store),
        joinedload(Invoice.lines)
    ).order_by(Invoice.date.desc()).all()

    for invoice in invoices:
        invoice.total_amount = sum(line.quantity * line.unit_price for line in invoice.lines)

    return render_template('invoices/index.html', invoices=invoices)

# Δημιουργία νέου τιμολογίου με αυτόματη αρίθμηση
@invoices_bp.route('/add', methods=['GET', 'POST'])
def add_invoice():
    form = InvoiceForm()

    if form.validate_on_submit():
        # Υπολογισμός επόμενου αριθμού τιμολογίου
        last_invoice = Invoice.query.order_by(Invoice.id.desc()).first()
        if last_invoice and last_invoice.number and last_invoice.number.startswith("INV-"):
            last_num = int(last_invoice.number.replace("INV-", ""))
            new_number = f"INV-{last_num + 1:04d}"
        else:
            new_number = "INV-0001"

        invoice = Invoice(
            number=new_number,
            date=form.date.data,
            client_id=form.client_id.data,
            store_id=form.store_id.data
        )
        db.session.add(invoice)
        db.session.flush()  # για να πάρει id

        for line_form in form.lines.entries:
            line = InvoiceLine(
                invoice_id=invoice.id,
                product_name=line_form.form.product_name.data,
                quantity=line_form.form.quantity.data,
                unit_price=line_form.form.unit_price.data
            )
            db.session.add(line)

        db.session.commit()
        flash("Το παραστατικό καταχωρήθηκε!", "success")
        return redirect(url_for('invoices.invoice_list'))  # Διορθώθηκε εδώ ✅

    return render_template('invoices/add.html', form=form)

# Προβολή συγκεκριμένου τιμολογίου
@invoices_bp.route('/<int:invoice_id>')
def view_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    return render_template('invoices/view.html', invoice=invoice)

# Εξαγωγή PDF (προβολή στο browser)
@invoices_bp.route('/<int:invoice_id>/pdf')
def export_invoice_pdf(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)

    # Δημιουργία QR Code
    qr = qrcode.make(f"Τιμολόγιο {invoice.number} - ID: {invoice.id}")
    qr_io = io.BytesIO()
    qr.save(qr_io, format='PNG')
    qr_data = base64.b64encode(qr_io.getvalue()).decode()

    rendered = render_template("invoices/pdf_template.html", invoice=invoice, qr_code_data=qr_data)
    pdf = HTML(string=rendered).write_pdf()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=invoice_{invoice.number}.pdf'
    return response

# Εξαγωγή PDF (λήψη αρχείου)
@invoices_bp.route('/<int:invoice_id>/download')
def download_invoice_pdf(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)

    qr = qrcode.make(f"Τιμολόγιο {invoice.number} - ID: {invoice.id}")
    qr_io = io.BytesIO()
    qr.save(qr_io, format='PNG')
    qr_data = base64.b64encode(qr_io.getvalue()).decode()

    rendered = render_template("invoices/pdf_template.html", invoice=invoice, qr_code_data=qr_data)
    pdf = HTML(string=rendered).write_pdf()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=invoice_{invoice.number}.pdf'
    return response