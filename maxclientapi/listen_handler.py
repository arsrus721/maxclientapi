# maxclientapi/listen_handler.py
from websocket import WebSocketConnectionClosedException
import json

def listen_handler(self):
        try:
            while self.running:
                try:
                    message = self.ws.recv()
                    json_load = json.loads(message)
                    opcode = json_load.get("opcode")

                    if opcode == 128:
                        text = json_load["payload"]["message"]["text"]
                        self.messages_128.put(text)
                        print(f"128! {text}")

                except WebSocketConnectionClosedException:
                    print("Connection closed")
                    break
                except Exception as e:
                    print(f"Unknown error: {e}")
                    continue
        finally:
            if self.ws:
                self.ws.close()
