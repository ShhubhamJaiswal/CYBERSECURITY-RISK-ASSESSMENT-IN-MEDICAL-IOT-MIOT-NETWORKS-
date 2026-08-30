"""
utils.py - shared helpers for attack simulation scripts
Enhanced with CSV logging and metrics.
"""

import hmac
import hashlib
import requests
import time
import csv
import os

# === CONFIGURATION ===

# --- FIX 1: This MUST be the full URL of your Cloud Function ---
CLOUD_FN = "https://us-central1-miot--project-9560d.cloudfunctions.net/ingestReading"

# --- FIX 2: This MUST match the secret in your Google Cloud Function ---
SECRET = b"YOUR_LONG_RANDOM_SECRET"  # Change this!

DEFAULT_DEVICE = "esp32-01"
LOG_DIR = "attack_logs"

# Ensure logs directory exists
os.makedirs(LOG_DIR, exist_ok=True)


def sign(deviceId, ts, nonce, tempC, hr, spo2):
    """Generate HMAC signature for canonical message."""
    canonical = f"{deviceId}|{ts}|{nonce}|{tempC}|{hr}|{spo2}"
    return hmac.new(SECRET, canonical.encode(), hashlib.sha256).hexdigest()


def send(payload, label="attack"):
    """Send POST request and log response."""
    start = time.time()
    try:
        # Use verify=False to bypass SSL errors if you're self-testing
        # In a real environment, you'd fix the certificate.
        # r = requests.post(CLOUD_FN, json=payload, timeout=5, verify=False)
        
        r = requests.post(CLOUD_FN, json=payload, timeout=5)
        elapsed = round((time.time() - start) * 1000, 2)
        log_result(label, payload["deviceId"], r.status_code, elapsed, r.text[:100])
        return r.status_code, r.text
    except Exception as e:
        log_result(label, payload["deviceId"], "ERR", 0, str(e))
        return None, str(e)


def log_result(label, deviceId, status, response_time, response):
    """Append results to CSV log file."""
    file_path = os.path.join(LOG_DIR, f"{label}_results.csv")
    new_file = not os.path.exists(file_path)
    with open(file_path, "a", newline="") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["timestamp", "deviceId", "status", "response_time(ms)", "response"])
        writer.writerow([int(time.time()), deviceId, status, response_time, response])