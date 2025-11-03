import json
import threading
import time
from websocket import create_connection, WebSocketConnectionClosedException

class ChatClient:
    def __init__(self, url, token, watch_chats=None, user_agent=None, deviceName=None, osVersion=None, deviceId=None):
        self.url = url or "wss://ws-api.oneme.ru/websocket"
        self.token = token
        self.watch_chats = watch_chats or []
        self.user_agent = user_agent or "PythonWebSocketClient/1.0"
        self.ws = None
        self.seq = 0
        self.running = False
        self.deviceName = deviceName or "Firefox"
        self.headerUserAgent = user_agent or "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:144.0) Gecko/20100101 Firefox/144.0"
        self.osVersion = osVersion or "Linux"
        self.deviceId = deviceId

    def connect(self):
        headers = [
            ("Origin", "https://web.max.ru"),
            ("User-Agent", self.user_agent)
        ]

        print(f"Preparing to connect to {self.url} with headers:")
        for header in headers:
            print(f"  {header[0]}: {header[1]}")
    
        try:
            print(f"Attempting to connect to WebSocket server at {self.url}...")
            self.ws = create_connection(self.url, header=[f"{h[0]}: {h[1]}" for h in headers])
            print("Connected!")
        
            self.running = True
        
            print("Sending handshake to the server...")
            self.send_info()
    
        except Exception as e:
            print(f"❌ Error during connection: {e}")
            self.running = False

    def send_info(self):
        payload = {"ver":11,
                   "cmd":0,
                   "seq":self.seq,
                   "opcode":6,
                   "payload":{
                       "userAgent":{
                           "deviceType":"WEB",
                           "locale":"ru",
                           "deviceLocale":"ru",
                           "osVersion":self.osVersion,
                           "deviceName":self.deviceName,
                           "headerUserAgent":self.headerUserAgent,
                           "appVersion":"25.11.1",
                           "screen":"1080x1920 1.0x",
                           "timezone":"Asia/Yekaterinburg"
                           },
                        "deviceId":self.deviceId
                        }
                    }
        self.send(payload)
        self.send_handshake()

    def send_handshake(self):
        self.seq += 1
        payload = {
            "ver": 11,
            "cmd": 0,
            "seq": self.seq,
            "opcode": 19,
            "payload": {
                "interactive": True,
                "token": self.token,
                "chatsCount": len(self.watch_chats),
                "chatsSync": 0,
                "contactsSync": 0,
                "presenceSync": 0,
                "draftsSync": 0
            }
        }
        self.send(payload)

    def subscribe_chat(self, chat_id):
        self.seq += 1
        payload = {"ver": 11, "cmd": 0, "seq": self.seq, "opcode": 65, "payload": {"chatId": chat_id, "type": "TEXT"}}
        self.send(payload)
        print(f"Subscribed to chat: {chat_id}")

    def send_message(self, chat_id, text):
        self.seq += 1
        payload = {
            "ver":11,
            "cmd":0,
            "seq":self.seq,
            "opcode":64,
            "payload":{
                "chatId":chat_id,
                "message":{
                    "text":text,
                    "cid":int(time.time()*1000),
                    "elements":[],
                    "attaches":[]
                },
                "notify":True
            }
        }

        self.send(payload)
        print(f"Message send to chat: {chat_id} with text: {text}")

    def send(self, data):
        if self.ws:
            try:
                self.ws.send(json.dumps(data))
                print(f"Data sent successfully: {json.dumps(data, indent=2)}")
            except Exception as e:
                print(f"Error sending data: {e}")
        else:
            print("No active WebSocket connection")


    def receive_loop(self, callback):
        try:
            while self.running:
                try:
                    message = self.ws.recv()
                except WebSocketConnectionClosedException:
                    print("WebSocket connection was closed")
                    break
                except Exception as e:
                    print(f"Unknown error: {e}")
                    continue

                if not message:
                    continue

                data = json.loads(message)
                callback(data)

        finally:
            self.ws.close()

    def start_keepalive(self, interval=30):
        def keepalive():
            while self.running:
                self.seq += 1
                ping_payload = {"ver": 11, "cmd": 0, "seq": self.seq, "opcode": 1, "payload": {"interactive": False}}
                try:
                    self.send(ping_payload)
                except:
                    break
                time.sleep(interval)
        threading.Thread(target=keepalive, daemon=True).start()

    def stop(self):
        self.running = False
        if self.ws:
            self.ws.close()