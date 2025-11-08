# Import necessary modules
import maxclientapi  # library for working with Max API (chat interaction)
import requests      # used for HTTP requests (uploading and sending files)

# Authorization token for API (identifies your client)
token = "YOUR TOKEN HERE"

# Unique device ID (used to identify your client instance)
deviceId = "DEVICE ID"

# Chat ID where the message will be sent
chat_id = CHAT ID without ""

# Path to the file that will be uploaded
file_path = "/path/to/your/file"

# Create a Max API client using the provided token and device ID
client1 = maxclientapi.ChatClient(token=token, deviceId=deviceId)

# Connect to the server
client1.connect()

# Start keepalive (sends periodic pings to keep the connection active)
client1.start_keepalive()

# Send a text message to the chat
client1.send_message(chat_id=chat_id, text="Hello")

# Subscribe to chat updates (so the client receives incoming messages)
client1.subscribe_chat(chat_id=chat_id)

# Request an upload URL for future file sending
client1.request_url_to_send_file()

# Main loop — continuously listens for new incoming messages
while True:
    msg = client1.get_message(block=True)  # Wait for a new message (blocking call)
    if not msg:
        continue  # Skip iteration if no message received

    # If the message is a download link
    if msg["type"] == "download_link":
        print(f"External {msg['EXTERNAL']}")
        print(f"video_url {msg['video_url']}")
        print(f"raw {msg['raw']}")

    # If the message contains a photo
    elif msg["type"] == "photo":
        print("chat_id", msg["chat_id"])
        print("sender", msg["sender"])
        print("id", msg["id"])
        print("time", msg["time"])
        print("utype", msg["utype"])
        print("baseUrl", msg["baseUrl"])
        print("previewData", msg["previewData"])
        print("photoToken", msg["photoToken"])
        print("width", msg["width"])
        print("photoId", msg["photoId"])
        print("height", msg["height"])
        print("raw", msg["raw"])

    # If the message contains a video
    elif msg["type"] == "video":
        print(f"chat_id {msg['chat_id']}")
        print(f"sender {msg['sender']}")
        print(f"thumbnail {msg['thumbnail']}")
        print(f"time {msg['duration']}")
        print(f"utype {msg['width']}")
        print(f"baseUrl {msg['videoId']}")
        print(f"previewData {msg['token']}")
        print(f"photoToken {msg['height']}")
        print(f"width {msg['raw']}")
        print(f"photoId {msg['id']}")
        print(f"height {msg['time']}")
        print(f"raw {msg['utype']}")
        print(f"raw {msg['prevMessageId']}")

        # Save the video token
        token_file = msg["token"]

        # Request the video URL for downloading
        client1.get_video_url(videoId=msg["videoId"], chat_id=chat_id, messageId=msg["id"])

    # If the message is a regular text message
    elif msg["type"] == "text":
        print("text", msg["text"])
        print("chat_id", msg["chat_id"])
        print("sender", msg["sender"])
        print("id", msg["id"])
        print("time", msg["time"])
        print("utype", msg["utype"])
        print("prevMessageId", msg["prevMessageId"])

    # If the server provides a URL for file upload
    elif msg["type"] == "url_upload":
        print(f"url {msg['url']}")
        print(f"token {msg['token']}")
        print(f"fileId {msg['fileId']}")

        token_file = msg["token"]  # Save upload token
        fileId = msg["fileId"]     # File ID assigned by the server

        # Open the local file and upload it to the provided URL
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f, "application/octet-stream")}  # Prepare file for POST
            headers = {"Authorization": f"Bearer {token_file}"}           # Include auth token
            response = requests.post(url=msg["url"], headers=headers, files=files)  # Upload file
            print("Response", response.status_code)  # Print HTTP response code

        # After the file is uploaded, send it to the chat
        client1.send_file(chatId=chat_id, fileId=fileId)
