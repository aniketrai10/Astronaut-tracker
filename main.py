import websocket
import json

# ==== HAR file se nikala hua WebSocket URL & headers (ready to use) ====
WS_URL = "wss://aviator-v2-vivo-casino.1wayez.life/socket.io/?EIO=3&transport=websocket"

HEADERS = {
    "Origin": "https://1wayez.life",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Cookie": "_ga=GA1.2.123456789.987654321; session=eyJpdiI6IjRweG1Yd1h1eHhQOTVPRmR0RnF4MVE9PSIsInZhbHVlIjoiWmJPRHVsQ0dYcEx3aFZzME9iYmpkYVhJeUhGcmNmaW4vU2VYUk1kSk9TQ05TR0dQa0F5UzZTRit6NGQ5M3BoMyIsIm1hYyI6IjRkMjQzZjE4ODc3ZTNhZGUxN2I1NjBhNDY1NjQxZmYzZjcwYjdmZjc1YmI3YTAxYmUwYzE5NTYwZDQyZTVmMDkifQ%3D%3D",
    "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
    "Sec-WebSocket-Version": "13",
    "Connection": "Upgrade",
    "Upgrade": "websocket"
}

def on_message(ws, message):
    print(f"RAW DATA: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### WebSocket closed ###")

def on_open(ws):
    print("Connected to WebSocket...")

if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        WS_URL,
        header=[f"{k}: {v}" for k, v in HEADERS.items()],
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    ws.run_forever()
