from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the database object
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configure the database URL
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://your_database_url_here"
    )

    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize the database with the app
    db.init_app(app)

    # Import your routes and models
    from . import routes, models
    app.register_blueprint(routes.api)

    return app

# Create and expose the Flask app instance for Gunicorn to use
app = create_app()
