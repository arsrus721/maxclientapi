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
                                if text == "":
                                    media_info = {
                                        "opcode": 128,
                                        "type": "photo",
                                        "chat_id": chat_id,
                                        "sender": sender,
                                        "id": message_data.get("id"),
                                        "time": message_data.get("time"),
                                        "utype": message_data.get("type"),
                                        "baseUrl": attach.get("baseUrl"),
                                        "previewData": attach.get("previewData"),
                                        "photoToken": attach.get("photoToken"),
                                        "width": attach.get("width"),
                                        "photoId": attach.get("photoId"),
                                        "height": attach.get("height"),
                                        "raw": attach
                                    }
                                    self.messages.put(media_info)
                                    print(f"Photo from {sender}")
                                else:
                                    media_info = {
                                        "opcode": 128,
                                        "type": "photo_with_text",
                                        "text": text,
                                        "chat_id": chat_id,
                                        "sender": sender,
                                        "id": message_data.get("id"),
                                        "time": message_data.get("time"),
                                        "utype": message_data.get("type"),
                                        "baseUrl": attach.get("baseUrl"),
                                        "previewData": attach.get("previewData"),
                                        "photoToken": attach.get("photoToken"),
                                        "width": attach.get("width"),
                                        "photoId": attach.get("photoId"),
                                        "height": attach.get("height"),
                                        "raw": attach
                                    }
                                    self.messages.put(media_info)
                                    print(f"Photo with text from {sender}")

                            elif media_type == "VIDEO":
                                if text == "":
                                    media_info = {
                                        "opcode": 128,
                                        "type": "video",
                                        "chat_id": chat_id,
                                        "sender": sender,
                                        "thumbnail": attach.get("thumbnail"),
                                        "duration": attach.get("duration"),
                                        "width": attach.get("width"),
                                        "videoId": attach.get("videoId"),
                                        "token": attach.get("token"),
                                        "height": attach.get("height"),
                                        "raw": attach,
                                        "id": message_data.get("id"),
                                        "time": message_data.get("time"),
                                        "utype": message_data.get("type"),
                                        "prevMessageId": payload.get("prevMessageId")
                                    }
                                    self.messages.put(media_info)
                                    print(f"Video from {sender}")
                                else:
                                    media_info = {
                                        "opcode": 128,
                                        "type": "video_with_text",
                                        "text": text,
                                        "chat_id": chat_id,
                                        "sender": sender,
                                        "thumbnail": attach.get("thumbnail"),
                                        "duration": attach.get("duration"),
                                        "width": attach.get("width"),
                                        "videoId": attach.get("videoId"),
                                        "token": attach.get("token"),
                                        "height": attach.get("height"),
                                        "raw": attach,
                                        "id": message_data.get("id"),
                                        "time": message_data.get("time"),
                                        "utype": message_data.get("type"),
                                        "prevMessageId": payload.get("prevMessageId")
                                    }
                                    self.messages.put(media_info)
                                    print(f"Video with text from {sender}")

                            elif media_type == "FILE":
                                media_info = {
                                    "opcode": 128,
                                    "type": "file",
                                    "chatId": chat_id,
                                    "sender": sender,
                                    "id": message_data.get("id"),
                                    "name": attach.get("name"),
                                    "size": attach.get("size"),
                                    "fileId": attach.get("fileId"),
                                    "token": attach.get("token")
                                }

                    elif text:
                        text_info = {
                            "opcode": 128,
                            "type": "text",
                            "chat_id": chat_id,
                            "sender": sender,
                            "text": text,
                            "id": message_data.get("id"),
                            "time": message_data.get("time"),
                            "utype": message_data.get("type"),
                            "prevMessageId": payload.get("prevMessageId")
                        }
                        self.messages.put(text_info)
                        print(f"Text from {sender}: {text}")

                elif opcode == 83:
                    payload = json_load.get("payload", {})
                    items_83 = list(payload.items())
                    download_info = {
                        "opcode": 83,
                        "type": "download_link",
                        "EXTERNAL": payload.get("EXTERNAL"),
                        "video_url": items_83[2][1],
                        "raw": payload
                    }
                    self.messages.put(download_info)
                    print("Gotted url")
                    
                elif opcode == 87:
                    url = json_load["payload"]["info"][0]["url"]
                    token = json_load["payload"]["info"][0]["token"]
                    fileId = json_load["payload"]["info"][0]["fileId"]
                    url_from_87 = {
                        "opcode": 87,
                        "type": "url_upload",
                        "url": url,
                        "token": token,
                        "fileId": fileId
                    }
                    self.messages.put(url_from_87)

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
