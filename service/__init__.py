from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sys

# Initialize the database object
db = SQLAlchemy()

def create_app():
    # Create and configure the Flask application
    app = Flask(__name__)

    # Use DATABASE_URL from environment, fallback to your Render DB (if not provided by Render)
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://accounts_db_7z73_user:ix3r5IlbmYB72Zio7KVGTNK6ffxe14VV@dpg-cvubj13e5dus73cie8t0-a.singapore-postgres.render.com/accounts_db_7z73"
    )

    # Fix legacy postgres:// scheme if needed
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    # Set the database URI and other configurations
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize the SQLAlchemy extension with the app
    db.init_app(app)

    # Import and register routes and models (avoiding circular imports)
    from . import routes, models
    app.register_blueprint(routes.api)

    # Log application startup
    app.logger.info(70 * "*")
    app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
    app.logger.info(70 * "*")

    try:
        # Initialize the database
        models.init_db(app)
    except Exception as error:
        app.logger.critical("%s: Cannot continue", error)
        sys.exit(4)

    # Adding security headers to all responses
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Content-Security-Policy'] = "default-src 'self'; object-src 'none'"
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response

    # Log that the service has been successfully initialized
    app.logger.info("Service initialized!")

    return app
