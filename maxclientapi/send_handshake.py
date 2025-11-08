# maxclientapi/send_handshake.py

def send_handshake(self):
        print("Sending handshake")
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
        self.send(payload, send_type="Handshake")