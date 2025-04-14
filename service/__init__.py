"""
Package: service
Package for the application models and service routes
This module creates and configures the Flask app and sets up the logging
and SQL database
"""
import sys
from flask import Flask
from service import config
from service.common import log_handlers
from flask_talisman import Talisman
from flask_cors import CORS

# Create Flask application
app = Flask(__name__)
app.config.from_object(config)

# Initialize Talisman to handle security headers
talisman = Talisman(app)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

# Import routes and models after app creation
from service import routes, models  # noqa: F401 E402

# Import error handlers and CLI commands
from service.common import error_handlers, cli_commands  # noqa: F401 E402

# Set up logging for production environment
log_handlers.init_logging(app, "gunicorn.error")

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

# Make sure to expose the 'app' variable to be used in the entry point
if __name__ == "__main__":
    app.run(debug=True)
