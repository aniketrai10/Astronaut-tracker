import socketio
import telegram
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

# Telegram setup
BOT_TOKEN = "8250743662:AAEe1t7RNJjBPhQT5kJH3BBdjbeUg9dm2wk"
CHAT_ID = "7380981045"
bot = telegram.Bot(token=BOT_TOKEN)

# Google Sheet setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/15BMpzvFlYCjURPboHI19qCX4ypEXZ9qwBCsAmeE_Ne4/edit?usp=drivesdk").sheet1

# Socket.IO setup
sio = socketio.Client()

@sio.event
def connect():
    bot.send_message(chat_id=CHAT_ID, text="✅ Tracker Connected to Astronaut server.")

@sio.on('crash')  # <-- HAR से actual event name confirm करना होगा
def on_crash(data):
    crash_point = data.get('crashPoint')
    if crash_point:
        sheet.append_row([time.strftime('%Y-%m-%d %H:%M:%S'), crash_point])
        if crash_point < 2.0:
            bot.send_message(chat_id=CHAT_ID, text=f"⚠️ Low Crash Alert: {crash_point}x")
        if crash_point < 1.5:
            bot.send_message(chat_id=CHAT_ID, text=f"🚨 Very Low Crash: {crash_point}x")

@sio.event
def disconnect():
    bot.send_message(chat_id=CHAT_ID, text="❌ Disconnected. Reconnecting...")
    time.sleep(5)
    sio.connect(URL)

# Connect to the WebSocket
URL = "wss://<subdomain>.1wayez.life/socket.io/?EIO=4&transport=websocket"
sio.connect(URL)
sio.wait()
