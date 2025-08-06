import os
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# Памʼять: device_id -> {code, timestamp}
codes = {}
EXPIRATION_SECONDS = 900  # 15 хвилин

@app.route("/send", methods=["POST"])
def send_code():
    data = request.get_json()
    device = data.get("device")
    code = data.get("code")

    if not device or not code:
        return jsonify({"error": "device and code required"}), 400

    codes[device] = {
        "code": code,
        "timestamp": time.time()
    }
    return jsonify({"status": "ok", "saved": code})

@app.route("/get", methods=["GET"])
def get_code():
    device = request.args.get("device")
    entry = codes.get(device)

    if not entry:
        return jsonify({"error": "not found"}), 404

    if time.time() - entry["timestamp"] > EXPIRATION_SECONDS:
        del codes[device]
        return jsonify({"error": "expired"}), 410

    return jsonify({"code": entry["code"]})

@app.route("/", methods=["GET"])
def home():
    return "✅ API працює"

if __name__ == "__main__":
    app.run()
