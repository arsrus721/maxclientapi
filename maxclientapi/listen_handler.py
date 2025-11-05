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
                    if opcode == 48:
                        print(f"opcode 48 received! Message: {json.dumps(json_load, indent=2, ensure_ascii=False)}")
                    elif opcode == 128:
                        print(f"New message {json_load["payload"]["message"]["text"]}")
                    elif opcode is not None:
                        print(f"received opcode {opcode} Message: {json.dumps(json_load, indent=2, ensure_ascii=False)}")
                    else:
                        print(f"No opcode found in the message: {message}")

                except WebSocketConnectionClosedException:
                    print("Connection closed")
                    break
                except Exception as e:
                    print(f"Unknown error: {e}")
                    continue
        finally:
            if self.ws:
                self.ws.close()