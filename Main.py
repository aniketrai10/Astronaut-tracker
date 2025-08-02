import time
import requests
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Bot

# --- CONFIG ---
TELEGRAM_TOKEN = "8250743662:AAEe1t7RNJjBPhQT5kJH3BBdjbeUg9dm2wk"
CHAT_ID = "7380981045"
GOOGLE_SHEET_NAME = "Astronaut Tracker"
# ---------------

# Telegram bot
bot = Bot(token=TELEGRAM_TOKEN)

# Google Sheet auth
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open(GOOGLE_SHEET_NAME).sheet1

# Dummy data fetcher (replace with live game API/websocket)
def fetch_game_data():
    return {"multiplier": 1.2, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}

# Streak tracking
streak_2x = 0

while True:
    data = fetch_game_data()
    multiplier = data["multiplier"]
    timestamp = data["timestamp"]

    # Add to Google Sheet
    sheet.append_row([timestamp, multiplier])

    # Check streak
    if multiplier < 2:
        streak_2x += 1
    else:
        streak_2x = 0

    # Alerts
    if streak_2x == 5:
        bot.send_message(chat_id=CHAT_ID, text=f"⚠️ 5x sub-2 streak at {timestamp}")
    if streak_2x == 10:
        bot.send_message(chat_id=CHAT_ID, text=f"🚨 10x sub-2 streak at {timestamp}")
    if streak_2x == 20:
        bot.send_message(chat_id=CHAT_ID, text=f"🔥 20x sub-2 streak at {timestamp}")

    time.sleep(5)
