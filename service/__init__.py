from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sys

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Use DATABASE_URL from environment, fallback to local SQLite for dev
    database_url = os.getenv("DATABASE_URL", "sqlite:///development.db")
    
    # Adjust Render's PostgreSQL URL for SQLAlchemy (if needed)
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Import and register routes *inside* the create_app function
    from . import routes  # Import here to avoid circular import
    app.register_blueprint(routes.api)

    app.logger.info(70 * "*")
    app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
    app.logger.info(70 * "*")

    try:
        models.init_db(app)  # Initialize the database tables
    except Exception as error:  # Catch broad exceptions (e.g., database issues)
        app.logger.critical("%s: Cannot continue", error)
        sys.exit(4)

    # Add security headers to all responses
    @app.after_request
    def add_security_headers(response):
        """Function to add security headers to every response"""
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Content-Security-Policy'] = "default-src 'self'; object-src 'none'"
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response

    # Log that the service has started
    app.logger.info("Service initialized!")

    # Check if we can connect to the database and set up tables
    try:
        models.init_db(app)
    except Exception as error:  # Handle database connection issues
        app.logger.critical("%s: Cannot continue", error)
        sys.exit(4)

    return app

# Make sure to expose the 'app' variable to be used in the entry point
if __name__ == "__main__":
    app.run(debug=True)
