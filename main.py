import json
import time
import requests
import websocket
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# === CONFIG ===
TELEGRAM_BOT_TOKEN = "8250743662:AAEe1t7RNJjBPhQT5kJH3BBdjbeUg9dm2wk"
TELEGRAM_CHAT_ID = "7380981045"
GOOGLE_SHEET_KEY = "15BMpzvFlYCjURPboHI19qCX4ypEXZ9qwBCsAmeE_Ne4"

# === Google Sheets Setup ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(GOOGLE_SHEET_KEY).sheet1

# === Telegram Send Function ===
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    requests.post(url, data=payload)

# === Handle Messages from Websocket ===
def on_message(ws, message):
    try:
        data = json.loads(message)
        if "multiplier" in data:  # Game crash multiplier
            multiplier = data["multiplier"]
            ts = time.strftime('%Y-%m-%d %H:%M:%S')
            sheet.append_row([ts, multiplier])
            if multiplier >= 20:
                send_telegram(f"🚀 High Multiplier Alert! {multiplier}x")
            elif multiplier < 2:
                send_telegram(f"⚠️ Low Multiplier: {multiplier}x")
    except Exception as e:
        print("Error:", e)

def on_error(ws, error):
    print("WebSocket error:", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed, retrying...")
    time.sleep(5)
    connect_ws()

def connect_ws():
    ws = websocket.WebSocketApp(
        "wss://1wayez.life/live-data-endpoint",  # Actual endpoint (HAR file based)
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

if __name__ == "__main__":
    send_telegram("✅ Astronaut Tracker Started")
    connect_ws()
