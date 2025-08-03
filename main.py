import asyncio
import websockets
import json
import time
import telegram
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Telegram setup
BOT_TOKEN = "8250743662:AAEe1t7RNJjBPhQT5kJH3BBdjbeUg9dm2wk"
CHAT_ID = "7380981045"
bot = telegram.Bot(token=BOT_TOKEN)

# Google Sheet setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/15BMpzvFlYCjURPboHI19qCX4ypEXZ9qwBCsAmeE_Ne4/edit?usp=drivesdk").sheet1

async def connect():
    url = "wss://1wayez.life/live/game-data"  # <-- HAR से निकला सही socket URL डालना पड़ेगा
    while True:
        try:
            async with websockets.connect(url, ping_interval=20, ping_timeout=20) as ws:
                await bot.send_message(chat_id=CHAT_ID, text="✅ Tracker Connected to Server.")
                while True:
                    msg = await ws.recv()
                    data = json.loads(msg)

                    # Extract crash point (modify if actual key name differs)
                    crash_point = data.get("crashPoint", None)
                    if crash_point:
                        sheet.append_row([time.strftime('%Y-%m-%d %H:%M:%S'), crash_point])
                        
                        # Alerts
                        if crash_point < 2.0:
                            await bot.send_message(chat_id=CHAT_ID, text=f"⚠️ Low Crash Alert: {crash_point}x")
                        if crash_point < 1.5:
                            await bot.send_message(chat_id=CHAT_ID, text=f"🚨 Very Low Crash: {crash_point}x")

        except websockets.ConnectionClosedError:
            await bot.send_message(chat_id=CHAT_ID, text="❌ Connection lost. Reconnecting...")
            await asyncio.sleep(5)
        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"Error: {str(e)}")
            await asyncio.sleep(10)

asyncio.run(connect())
