from flask import Flask, request, jsonify
import sqlite3
import uuid
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "device_events.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS device_events (
            id TEXT PRIMARY KEY,
            device_id TEXT NOT NULL,
            status TEXT,
            timestamp TEXT,
            payload TEXT
        )
        """
    )
    conn.commit()
    conn.close()

app = Flask(__name__)
init_db()

@app.route('/devices/<device_id>/status', methods=['POST'])
def device_status(device_id):
    # Accept JSON payload
    data = request.get_json(silent=True) or {}
    status = data.get('status')
    timestamp = data.get('timestamp') or datetime.utcnow().isoformat()
    payload = data.get('payload')

    event_id = str(uuid.uuid4())

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        'INSERT INTO device_events (id, device_id, status, timestamp, payload) VALUES (?, ?, ?, ?, ?)',
        (event_id, device_id, status, timestamp, str(payload))
    )
    conn.commit()
    conn.close()

    return jsonify({"ok": True, "id": event_id}), 201

@app.route('/devices/events', methods=['GET'])
def list_events():
    # optional query param limit
    limit = request.args.get('limit', default=100, type=int)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, device_id, status, timestamp, payload FROM device_events ORDER BY timestamp DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()

    events = [
        {"id": r[0], "device_id": r[1], "status": r[2], "timestamp": r[3], "payload": r[4]} for r in rows
    ]
    return jsonify(events)

if __name__ == '__main__':
    # Run on port 5001 so it doesn't conflict with Streamlit default 8501
    app.run(host='0.0.0.0', port=5001)
