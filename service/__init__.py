from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sys

# Initialize the database object
db = SQLAlchemy()

def create_app(environ=None, start_response=None):
    app = Flask(__name__)

    # Use DATABASE_URL from environment or fallback
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://accounts_db_7z73_user:ix3r5IlbmYB72Zio7KVGTNK6ffxe14VV@dpg-cvubj13e5dus73cie8t0-a.singapore-postgres.render.com/accounts_db_7z73"
    )

    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Import routes and models after db initialization
    from . import routes, models
    app.register_blueprint(routes.api)

    # Log initialization message
    app.logger.info(70 * "*")
    app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
    app.logger.info(70 * "*")

    # Initialize the database
    try:
        models.init_db(app)
    except Exception as error:
        app.logger.critical("%s: Cannot continue", error)
        sys.exit(4)

    # Security headers
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Content-Security-Policy'] = "default-src 'self'; object-src 'none'"
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return
