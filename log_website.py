from flask import Flask, request, jsonify
import logging
import random
import psutil
from datetime import datetime

app = Flask(__name__)

# Configure logging to write to a file
logging.basicConfig(
    filename="website_logs.json",
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
)

# Helper function to log messages
def log_event(level, message, extra_data=None):
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "message": message,
        **(extra_data or {}),
    }
    app.logger.info(log_data)


# ROUTES FOR DIFFERENT LOG TYPES

# 1. Application Logs
@app.route('/')
def home():
    log_event("INFO", "Accessed Home Page", {"endpoint": "/", "status": "success"})
    return "Welcome to the Home Page!"


@app.route('/api', methods=["GET"])
def api_request():
    response_time = random.randint(100, 1000)  # Simulating response time in ms
    log_event("INFO", "API request received", {
        "endpoint": "/api",
        "status": "success",
        "response_time_ms": response_time,
    })
    return jsonify({"message": "API response", "response_time_ms": response_time})


# 2. System Logs
@app.route('/system')
def system_logs():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    log_event("INFO", "System health checked", {
        "endpoint": "/system",
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
    })
    return jsonify({"cpu_usage": cpu_usage, "memory_usage": memory_usage})


# 3. Security Logs
@app.route('/login', methods=["POST"])
def login():
    user = request.form.get("username", "unknown_user")
    success = random.choice([True, False])  # Simulate login success or failure
    event_type = "LOGIN_SUCCESS" if success else "LOGIN_FAILURE"
    log_event("INFO", f"User login attempt: {event_type}", {
        "username": user,
        "status": "success" if success else "failure",
    })
    return "Login Successful!" if success else "Login Failed!"


@app.route('/suspicious', methods=["GET"])
def suspicious_activity():
    ip_address = request.remote_addr
    log_event("WARNING", "Suspicious activity detected", {"ip_address": ip_address})
    return "Suspicious activity logged."


# 4. Business/Operational Logs
@app.route('/purchase', methods=["POST"])
def purchase():
    user = request.form.get("username", "anonymous")
    product = request.form.get("product", "unknown_product")
    amount = random.randint(10, 1000)  # Simulate transaction amount
    log_event("INFO", "Purchase made", {
        "user": user,
        "product": product,
        "amount": amount,
        "transaction_id": random.randint(10000, 99999),
    })
    return jsonify({"message": "Purchase successful", "product": product, "amount": amount})


# Simulate generating many logs for testing
@app.route('/generate-logs')
def generate_logs():
    for _ in range(10):
        log_event("INFO", "Generated bulk logs for testing")
    return "Bulk logs generated."


# 404 Error Logging
@app.errorhandler(404)
def not_found(error):
    log_event("ERROR", "404 error", {"path": request.path})
    return jsonify({"error": "Not Found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
