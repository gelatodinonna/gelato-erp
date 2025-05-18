import os

class Config:
    # Secret key for session and CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secret-key')

    # Support for SQLite (dev) and Postgres (production)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///gelato_erp.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Optional: For Flask-WTF if you want to disable CSRF in testing
    WTF_CSRF_ENABLED = True