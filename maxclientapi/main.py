import json
import threading
import time
from websocket import create_connection, WebSocketConnectionClosedException
from .listen_handler import listen_handler
from .start_keepalive import start_keepalive
from .send_handshake import send_handshake

class ChatClient:
    def __init__(self, token, deviceId, watch_chats=None, user_agent=None, deviceName=None, osVersion=None, origin=None, url=None):
        self.url = url or "wss://ws-api.oneme.ru/websocket"
        self.token = token
        self.watch_chats = watch_chats or []
        self.user_agent = user_agent or "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:144.0) Gecko/20100101 Firefox/144.0"
        self.ws = None
        self.seq = 0
        self.running = False
        self.deviceName = deviceName or "Firefox"
        self.headerUserAgent = user_agent
        self.osVersion = osVersion or "Linux"
        self.deviceId = deviceId
        self.origin = origin or "https://web.max.ru"

    def connect(self):
        headers = [
            ("Origin", self.origin),
            ("User-Agent", self.user_agent)
        ]
    
        try:
            print(f"Try to connect to {self.url}")
            self.ws = create_connection(self.url, header=[f"{h[0]}: {h[1]}" for h in headers])
            print("Connected")
        
            self.running = True
        
            threading.Thread(target=self.listen_handler, daemon=True).start()

            print(" Sending handshake")
            self.send_info()
    
        except Exception as e:
            print(f"Unknown error: {e}")
            self.running = False

    def send_info(self):
        print("send info")
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

    send_handshake = send_handshake

    def request_messages(self):
        self.seq += 1
        payload = {"ver":11,
                   "cmd":0,
                   "seq":self.seq,
                   "opcode":48,
                   "payload":{
                       "chatIds":[0]
                       }
                    }
        
        self.send(payload)

    listen_handler = listen_handler

    def subscribe_chat(self, chat_id):
        self.seq += 1
        payload = {"ver":11,
                   "cmd":0,
                   "seq":self.seq,
                   "opcode":75,
                   "payload":{
                       "chatId":chat_id,
                       "subscribe":True
                       }
                    }
        self.send(payload)
        print(f"Subscribed to chat: {chat_id}")

    def send_message(self, chat_id, text):
        self.seq += 1
        payload = {
            "ver": 11,
            "cmd": 0,
            "seq": self.seq,
            "opcode": 64,
            "payload": {
                "chatId": chat_id,
                "message": {
                    "text": text,
                    "cid": int(time.time() * 1000),
                    "elements": [],
                    "attaches": []
                },
                "notify": True
            }
        }

        self.send(payload)
        print(f"Message send to chat: {chat_id} with text: {text}")
        self.seq += 1
        payload_1 = {"ver":11,
                     "cmd":0,
                     "seq":self.seq,
                     "opcode":177,
                     "payload":{
                         "chatId":chat_id,
                         "time":0
                         }
                    }
        self.send(payload_1)

    def send(self, data):
        if self.ws:
            try:
                self.ws.send(json.dumps(data))
                print(f"Data sucessfully sent: {json.dumps(data, indent=2)}")
            except Exception as e:
                print(f"Unknown error: {e}")
        else:
            print("No active WebSocket connection")

    start_keepalive = start_keepalive

    def stop(self):
        self.running = False
        if self.ws:
            self.ws.close()