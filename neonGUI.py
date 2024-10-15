"""
Main body of code. Execute to start program.
"""

import json
import threading
import time
from api import Api, ApiRecv, InfoApi
from app import App
from entities import Match


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

        self.api = Api(self.api_address, self.api_port)
        self.api_recv = ApiRecv(self.match, self.api_address, self.api_recv_port)
        self.info_api = InfoApi(self.match, self.match.robots, self.match.opposites, self.match.ball,
                                self.match.control_parameters, self.match.coach_name)

    def start(self):
        self.api.start()
        self.api_recv.connect_info(self.info_api)
        self.api_recv.start()

        self.main_thread = threading.current_thread()

        self.update_thread = threading.Thread(target=self.update)
        self.update_thread.start()

        self.app.start()

    def update(self):
        while self.main_thread.is_alive():
            # self.api.send_data(self.info_api)
            self.api.send_gui_info()

gui = NeonFCGUI()
gui.start()
