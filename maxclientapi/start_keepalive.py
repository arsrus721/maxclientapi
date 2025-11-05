# maxclientapi/start_keepalive.py
import threading
import time

def start_keepalive(self, interval=25):
        def keepalive():
            while self.running:
                self.seq += 1
                ping_payload = {"ver": 11,
                                "cmd": 0,
                                "seq": self.seq,
                                "opcode": 1,
                                "payload": {
                                    "interactive": False
                                    }
                                }
                try:
                    self.send(ping_payload)
                except:
                    break
                time.sleep(interval)
        threading.Thread(target=keepalive, daemon=True).start()