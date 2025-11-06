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
                    payload = json_load.get("payload", {})
                    message_data = payload.get("message", {})
                    chat_id = payload.get("chatId")
                    sender = message_data.get("sender")

                    attaches = message_data.get("attaches")
                    text = message_data.get("text")

                    if attaches:
                        for attach in attaches:
                            media_type = attach.get("_type")

                            if media_type == "PHOTO":
                                media_info = {
                                    "opcode": 128,
                                    "type": "photo",
                                    "chat_id": chat_id,
                                    "sender": sender,
                                    "url": attach.get("baseUrl"),
                                    "preview": attach.get("previewData"),
                                    "width": attach.get("width"),
                                    "height": attach.get("height"),
                                    "raw": attach
                                }
                                self.messages_128.put(media_info)
                                print(f"Photo from {sender}: {attach.get('baseUrl')}")

                            elif media_type == "VIDEO":
                                message_id = message_data.get("id")
                                media_info = {
                                    "opcode": 128,
                                    "type": "video",
                                    "chat_id": chat_id,
                                    "sender": sender,
                                    "thumbnail": attach.get("thumbnail"),
                                    "duration": attach.get("duration"),
                                    "width": attach.get("width"),
                                    "videoId": attach.get("videoId"),
                                    "height": attach.get("height"),
                                    "raw": attach,
                                    "id": message_id
                                }

                                self.messages_128.put(media_info)
                                print(f"Video from {sender}: {attach.get('thumbnail')}")

                    elif text:
                        text_info = {
                            "opcode": 128,
                            "type": "text",
                            "chat_id": chat_id,
                            "sender": sender,
                            "text": text
                        }
                        self.messages_128.put(text_info)
                        print(f"Text from {sender}: {text}")

                elif opcode == 83:
                    payload = json_load.get("payload", {})
                    external_url = payload.get("EXTERNAL")
                    mp4_1080 = payload.get("MP4_1080")

                    download_info = {
                        "opcode": 83,
                        "type": "download_link",
                        "external_url": external_url,
                        "mp4_1080": mp4_1080,
                        "raw": payload
                    }
                    self.messages_128.put(download_info)
                    print(f"Gotted url:\n"
                          f"   Page: {external_url}\n"
                          f"   URL: {mp4_1080}")

            except WebSocketConnectionClosedException:
                print("Connection closed")
                break
            except Exception as e:
                print(f"Unknown error: {e}")
                continue

    finally:
        if self.ws:
            self.ws.close()
            print("ws closed")
