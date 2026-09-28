import os
import socket
import datetime
from flask import Flask, jsonify, render_template

# Initialize Flask application
app = Flask(__name__)

# Application Configuration (can be overridden via environment variables)
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_ENV = os.getenv("APP_ENV", "production")
PORT = int(os.getenv("PORT", 5000))
START_TIME = datetime.datetime.now(datetime.timezone.utc)

@app.route("/")
def index():
    """Renders the DevOps landing dashboard template."""
    hostname = socket.gethostname()
    current_time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    return render_template(
        "index.html",
        version=APP_VERSION,
        environment=APP_ENV,
        hostname=hostname,
        current_time=current_time
    )

@app.route("/health")
def health():
    """Health check endpoint used by Docker and CI/CD pipelines to verify app status."""
    uptime_seconds = (datetime.datetime.now(datetime.timezone.utc) - START_TIME).total_seconds()
    return jsonify({
        "status": "healthy",
        "version": APP_VERSION,
        "environment": APP_ENV,
        "uptime_seconds": round(uptime_seconds, 2),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }), 200

@app.route("/api/info")
def info():
    """API endpoint providing system and container metadata."""
    return jsonify({
        "app_name": "Automated Docker Deployment App",
        "version": APP_VERSION,
        "environment": APP_ENV,
        "hostname": socket.gethostname(),
        "start_time_utc": START_TIME.isoformat(),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors with a structured JSON response."""
    return jsonify({
        "error": "Not Found",
        "message": "The requested resource could not be found.",
        "status_code": 404
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 Method Not Allowed errors with a structured JSON response."""
    return jsonify({
        "error": "Method Not Allowed",
        "message": "The method is not allowed for the requested URL.",
        "status_code": 405
    }), 405

@app.errorhandler(500)
def internal_server_error(error):
    """Handle 500 Internal Server Error with a structured JSON response."""
    return jsonify({
        "error": "Internal Server Error",
        "message": "An internal server error occurred.",
        "status_code": 500
    }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
