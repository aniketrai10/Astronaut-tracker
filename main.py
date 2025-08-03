import websocket
import json
import time
from datetime import datetime
import telegram

# ==== CONFIG ====
BOT_TOKEN = "8250743662:AAEe1t7RNJjBPhQT5kJH3BBdjbeUg9dm2wk"  # Tumhara saved bot token
CHAT_ID = "7380981045"  # Tumhara saved chat ID
WS_URL = "wss://1wayez.life/socket.io/?EIO=3&transport=websocket"  # Real Astronaut WebSocket
DATA_FILE = "data.txt"
ALERT_MULTIPLIERS = [5, 10, 15, 20]  # Alerts ke liye

# Telegram bot setup
bot = telegram.Bot(token=BOT_TOKEN)

def log_data(crash_point):
    """Save crash points to file with timestamp"""
    with open(DATA_FILE, "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Crash: {crash_point}x\n")

def send_alert(crash_point):
    """Send Telegram alerts on certain multipliers"""
    for m in ALERT_MULTIPLIERS:
        if crash_point >= m:
            bot.send_message(chat_id=CHAT_ID, text=f"🚀 Astronaut Crash Alert: {crash_point}x!")

def on_message(ws, message):
    try:
        if message.startswith("42"):  # Socket.io message format
            payload = json.loads(message[2:])
            if isinstance(payload, list) and len(payload) > 1:
                data = payload[1]
                if "crashPoint" in data:
                    crash_point = float(data["crashPoint"])
                    log_data(crash_point)
                    send_alert(crash_point)
                    print(f"Crash: {crash_point}x")
    except Exception as e:
        print("Error parsing:", e)

def on_error(ws, error):
    print("WebSocket Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket Closed. Reconnecting in 5s...")
    time.sleep(5)
    connect()

def on_open(ws):
    print("WebSocket Connected!")

def connect():
    ws = websocket.WebSocketApp(WS_URL,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    connect()
