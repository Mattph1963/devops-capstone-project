from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

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

    return app
