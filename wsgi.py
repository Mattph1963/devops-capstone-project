"""
Entry point for running the Flask application.
This file is used by Gunicorn or for running locally.
"""

from service import app  # Import the Flask app from the service package

# Run the Flask app only if this script is executed directly (e.g. python wsgi.py)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
