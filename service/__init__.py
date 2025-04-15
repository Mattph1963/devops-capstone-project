from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sys

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Use DATABASE_URL from environment, fallback to your Render DB
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://your_database_url_here"
    )

    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from . import routes, models
    app.register_blueprint(routes.api)

    app.logger.info(70 * "*")
    app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
    app.logger.info(70 * "*")

    try:
        models.init_db(app)
    except Exception as error:
        app.logger.critical("%s: Cannot continue", error)
        sys.exit(4)

    @app.after_request
    def add_security_headers(response):
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Content-Security-Policy'] = "default-src 'self'; object-src 'none'"
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response

    app.logger.info("Service initialized!")

    return app
