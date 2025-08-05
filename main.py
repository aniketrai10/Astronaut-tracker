import websocket
import json
import time

def on_message(ws, message):
    print("Raw Response:", message)  # Debugging ke liye pura response print
    try:
        data = json.loads(message)
        print("Parsed JSON:", data)   # Parsed JSON bhi print kare
    except:
        print("JSON parse error")
    
def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")

def on_open(ws):
    print("Connected to WebSocket")

if __name__ == "__main__":
    while True:
        try:
            ws = websocket.WebSocketApp(
                "wss://<Yaha Tumhara WebSocket URL Daalo>",
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            ws.run_forever()
        except Exception as e:
            print("Connection failed, retrying...", e)
            time.sleep(5)
