from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_PATH = "/home/halfdan/mywebapp/data.db"

# --- Initialize database at startup ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
CREATE TABLE IF NOT EXISTS sensor_data (
    lokale INTEGER PRIMARY KEY,
    lysniveau INTEGER,
    timestamp TEXT
)
    ''')
    conn.commit()
    conn.close()

# Run init_db when the module is imported
init_db()

# --- Route to receive data from ESP32 ---
@app.route("/data", methods=["POST"])
def receive_data():
    data = request.get_json()
    print("Received:", data)

    if not data or "lokale" not in data or "lysniveau" not in data:
        return jsonify({"error": "Invalid data format"}), 400

    lokale = data["lokale"]
    lysniveau = data["lysniveau"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO sensor_data (lokale, lysniveau, timestamp)
            VALUES (?, ?, ?)
            ON CONFLICT(lokale) DO UPDATE SET
                lysniveau = excluded.lysniveau,
                timestamp = excluded.timestamp
        ''', (lokale, lysniveau, timestamp))
        conn.commit()
        conn.close()
        return jsonify({"status": "saved or updated"}), 200

    except Exception as e:
        print("DB Error:", e)
        return jsonify({"error": str(e)}), 500



# Hent gemt data
@app.route("/get_data", methods=["GET"])
def get_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM sensor_data")
        rows = [dict(row) for row in c.fetchall()]
        conn.close()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
