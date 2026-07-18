import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Device Events", layout="wide")

st.title("🔌 Device Events")
st.markdown("Shows recent device status updates (from IoT devices).")

DB_PATH = "device_events.db"

def load_events(limit=100):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT device_id, status, timestamp, payload FROM device_events ORDER BY timestamp DESC LIMIT ?', (limit,))
        rows = c.fetchall()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"Error reading device events DB: {e}")
        return []

cols = st.columns([1, 1, 6])
with cols[0]:
    limit = st.number_input("Limit", min_value=1, max_value=1000, value=100)
with cols[1]:
    # Pressing the button will re-run the script automatically in Streamlit
    refresh = st.button("Refresh Events")

events = load_events(limit)

if not events:
    st.info("No device events recorded yet. Devices can POST to /devices/<device_id>/status on port 5001.")
else:
    for device_id, status, ts, payload in events:
        try:
            dt = datetime.fromisoformat(ts)
            ts_str = dt.strftime("[%H:%M, %d/%m/%Y]")
        except Exception:
            ts_str = f"[{ts}]"
        extra = f" - {payload}" if payload and payload != 'None' else ""
        st.write(f"{ts_str} {device_id}: {status}{extra}")

    # Quick demo button: use the latest device event's payload in the Crop page
    latest = events[0]
    latest_device_id, latest_status, latest_ts, latest_payload = latest[0], latest[1], latest[2], latest[3]
    if latest_payload:
        if st.button("Use latest sample in Crop page"):
            opt_str = f"{latest_ts} | {latest_device_id} | {latest_status} | {latest_payload}"
            st.session_state['device_event_select_crop'] = opt_str
            st.success("Latest sample set for Crop page. Switch to Crop Recommendation to see it attached.")
    else:
        st.info("Latest event has no payload to attach to Crop page.")

st.markdown("---")
st.markdown("""How to send events from a device or curl:

```
curl -X POST http://<server-host>:5001/devices/DEVICE_ID/status \
  -H 'Content-Type: application/json' \
  -d '{"status": "ready", "timestamp": "2026-07-18T07:50:00Z", "payload": "sample_id=123"}'
```
""")