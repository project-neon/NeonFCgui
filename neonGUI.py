"""
Main body of code. Execute to start program.
"""

import json
import threading
import time
from app import App
from entities import Match
from neonfc_client import NeonFCClient

def get_config(config_file=None):
    if config_file:
        config = json.loads(open(config_file, 'r').read())
    else:
        config = json.loads(open('config.json', 'r').read())

    return config

class NeonFCGUI(object):
    def __init__(self, config_file=None):
        self.main_thread = None
        self.update_thread = None

        # Log file for the last session shall be emptied
        log_file = open("files/last_session_log.txt", "w")
        log_file.write("Last session started at: ")
        log_file.write(str(time.ctime(time.time())) + "\n")
        log_file.close()

        self.match = Match()
        self.app = App(self)

        self.config = get_config(config_file)

        self.api_address = self.config.get("network").get("api_address")
        self.api_port = self.config.get("network").get("api_port")
        self.api_recv_port = self.config.get("network").get("api_recv_port")

        self.api_client = NeonFCClient("localhost", self.api_recv_port)

    def start(self):
        self.api_client.start()

        self.main_thread = threading.current_thread()

        self.update_thread = threading.Thread(target=self.update)
        self.update_thread.start()

        self.app.start()

    def update(self):
        while self.main_thread.is_alive():
            try:
                tracking = self.api_client.get_tracking().tracking
                robots = tracking.robots
                opposites = tracking.opposites

                self.match.team_color = "blue" if opposites[0].color == 1 else "yellow"

                self.match.ball.update_information(tracking.ball)

                for r in robots[:6]:
                    if self.match.robots[r.id]:
                        self.match.robots[r.id].update_information(r)

                for o in opposites[:6]:
                    if self.match.opposites[o.id]:
                        self.match.opposites[o.id].update_information(o)

            except Exception as e:
                print(e)

            time.sleep(0.001)  # Necessary pause of 1ms to avoid busy waiting (https://superfastpython.com/thread-busy-waiting-in-python/)
            # self.api.send_gui_info()

gui = NeonFCGUI()
gui.start()
