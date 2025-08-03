import websocket
import json
from telegram import Bot
from flask import Flask, send_file
import threading
from datetime import datetime

# ==== Telegram Setup ====
TELEGRAM_BOT_TOKEN = "yaha_apna_token"
CHAT_ID = "yaha_apna_chatid"
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# ==== Flask App for data.txt ====
app = Flask(__name__)

@app.route("/data.txt")
def get_data():
    return send_file("data.txt")

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# ==== WebSocket Callbacks ====
def on_message(ws, message):
    try:
        data = json.loads(message)
        if "multiplier" in data:
            multiplier = data["multiplier"]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Write to data.txt
            with open("data.txt", "a") as f:
                f.write(f"[{timestamp}] Multiplier: {multiplier}x\n")

            # Telegram Alert for >=20x
            if multiplier >= 20:
                bot.send_message(chat_id=CHAT_ID, text=f"🚀 High Multiplier Alert: {multiplier}x")

            print(f"[{timestamp}] Multiplier: {multiplier}x")
    except Exception as e:
        print(f"Error: {e}")

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")

def on_open(ws):
    print("WebSocket connection opened")

# ==== Start WebSocket ====
def start_ws():
    ws = websocket.WebSocketApp(
        "wss://<exact_websocket_url>",  # <-- yaha tumhara actual websocket URL dalega
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    start_ws()
