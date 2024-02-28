"""
Main body of code. Execute to start program.
"""

from app import App
from api import Api, Api_recv, Info_Api
from entities import Match
import json
import threading
import time

def get_config(config_file = None):
    if config_file:
        config = json.loads(open(config_file, 'r').read())
    else:
        config = json.loads(open('config.json', 'r').read())

    return config

class GUI(object):
    def __init__(self, config_file = None):
        self.match = Match()
        self.app = App(self)

        self.config = get_config(config_file)    

        self.api_address = self.config.get("network").get("api_address")
        self.api_port = self.config.get("network").get("api_port")
        self.api_recv_port = self.config.get("network").get("api_recv_port")

        self.api = Api(self.api_address, self.api_port)
        self.api_recv = Api_recv(self.match, self.api_address, self.api_recv_port)
        self.info_api = Info_Api(self.match, self.match.robots, self.match.opposites, self.match.ball, self.match.control_parameters, self.match.coach_name)

    
    def start(self):
        self.api.start()
        self.api_recv.connect_info(self.info_api)
        self.api_recv.start()

        self.update_thread = threading.Thread(target=self.update)
        self.update_thread.start()

        while not self.update_thread.is_alive():
            time.sleep(0.1)

        self.app.start()
        print(self.info_api.data)

    def update(self):
        while True:
            self.api.send_data(self.info_api)

        
gui = GUI()
gui.start()