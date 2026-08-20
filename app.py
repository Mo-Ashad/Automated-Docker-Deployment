import os
import socket
import datetime
from flask import Flask, jsonify, render_template_string

# Initialize Flask application
app = Flask(__name__)

# Application Configuration (can be overridden via environment variables)
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_ENV = os.getenv("APP_ENV", "production")
PORT = int(os.getenv("PORT", 5000))
START_TIME = datetime.datetime.now(datetime.timezone.utc)

# Embedded HTML Template for a clean, beginner-friendly DevOps status dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Automated Docker Deployment</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        body {
            background-color: #0f172a;
            color: #f8fafc;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            background: #1e293b;
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.5);
            max-width: 650px;
            width: 100%;
            padding: 32px;
            border: 1px solid #334155;
        }
        .header {
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 24px;
            border-bottom: 1px solid #334155;
            padding-bottom: 20px;
        }
        .badge-icon {
            font-size: 40px;
            background: #0284c7;
            border-radius: 12px;
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        h1 {
            font-size: 22px;
            font-weight: 700;
            color: #ffffff;
        }
        .subtitle {
            color: #94a3b8;
            font-size: 14px;
            margin-top: 4px;
        }
        .status-banner {
            background: rgba(34, 197, 94, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.3);
            color: #4ade80;
            padding: 12px 16px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 24px;
            font-weight: 500;
            font-size: 15px;
        }
        .pulse-dot {
            width: 10px;
            height: 10px;
            background-color: #22c55e;
            border-radius: 50%;
            box-shadow: 0 0 10px #22c55e;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.2); opacity: 1; }
            100% { transform: scale(0.95); opacity: 0.8; }
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }
        .card {
            background: #0f172a;
            padding: 16px;
            border-radius: 10px;
            border: 1px solid #334155;
        }
        .card-label {
            font-size: 12px;
            text-transform: uppercase;
            color: #64748b;
            font-weight: 600;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }
        .card-value {
            font-size: 16px;
            color: #f1f5f9;
            font-family: monospace;
            word-break: break-all;
        }
        .pipeline-info {
            background: #0f172a;
            padding: 16px;
            border-radius: 10px;
            border: 1px solid #334155;
            margin-bottom: 24px;
        }
        .pipeline-title {
            font-size: 13px;
            color: #38bdf8;
            font-weight: 600;
            margin-bottom: 8px;
        }
        .pipeline-steps {
            font-size: 13px;
            color: #cbd5e1;
            line-height: 1.6;
        }
        .endpoints {
            display: flex;
            gap: 12px;
        }
        .btn {
            flex: 1;
            text-align: center;
            padding: 10px 16px;
            border-radius: 8px;
            text-decoration: none;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        .btn-primary {
            background: #0284c7;
            color: white;
        }
        .btn-primary:hover {
            background: #0369a1;
        }
        .btn-secondary {
            background: #334155;
            color: #e2e8f0;
        }
        .btn-secondary:hover {
            background: #475569;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="badge-icon">🐳</div>
            <div>
                <h1>Automated Docker Deployment</h1>
                <div class="subtitle">DevOps CI/CD Pipeline Demo App</div>
            </div>
        </div>

        <div class="status-banner">
            <div class="pulse-dot"></div>
            <span>Container is running & healthy</span>
        </div>

        <div class="grid">
            <div class="card">
                <div class="card-label">App Version</div>
                <div class="card-value" style="color: #38bdf8;">v{{ version }}</div>
            </div>
            <div class="card">
                <div class="card-label">Environment</div>
                <div class="card-value" style="color: #facc15;">{{ environment }}</div>
            </div>
            <div class="card">
                <div class="card-label">Container / Hostname</div>
                <div class="card-value">{{ hostname }}</div>
            </div>
            <div class="card">
                <div class="card-label">Server Time (UTC)</div>
                <div class="card-value">{{ current_time }}</div>
            </div>
        </div>

        <div class="pipeline-info">
            <div class="pipeline-title">🚀 How this deployment worked:</div>
            <div class="pipeline-steps">
                1. Code pushed to GitHub repository<br>
                2. GitHub Actions ran automated unit tests (pytest)<br>
                3. Docker image built & pushed automatically<br>
                4. Automated deployment script restarted the container
            </div>
        </div>

        <div class="endpoints">
            <a href="/health" class="btn btn-primary">Health Check Endpoint (/health)</a>
            <a href="/api/info" class="btn btn-secondary">API Info Endpoint (/api/info)</a>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    """Renders the DevOps landing dashboard."""
    hostname = socket.gethostname()
    current_time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    return render_template_string(
        DASHBOARD_HTML,
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
