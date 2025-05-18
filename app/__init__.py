import os
from flask import Flask
from flask_migrate import Migrate
from .extensions import db, migrate, csrf
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Register blueprints
    from app.main.routes import main_bp
    from app.payroll.routes import payroll_bp
    from app.hr.routes import hr_bp
    from app.inventory.routes import inventory_bp
    from app.stores.routes import stores_bp
    from app.revenues.routes import revenues_bp
    from app.expenses.routes import expenses_bp
    from app.sales.routes import sales_bp
    from app.reports.routes import reports_bp
    from app.api.routes import api_bp
    from app.costing.routes import costing_bp
    from app.invoices.routes import invoices_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(payroll_bp)
    app.register_blueprint(hr_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(stores_bp)
    app.register_blueprint(revenues_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(costing_bp)
    app.register_blueprint(invoices_bp)

    return app