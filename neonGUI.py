"""
Main body of code. Execute to start program.
"""

from app import App
from api import Api, Api_recv, Info_Api
from entities import Match
import json

def get_config(config_file = None):
    if config_file:
        config = json.loads(open(config_file, 'r').read())
    else:
        config = json.loads(open('config.json', 'r').read())

    return config

class GUI(object):
    def __init__(self, config_file = None):
        self.app = App(self)
        self.match = Match()

        self.config = get_config(config_file)

        self.api_address = self.config.get("network").get("api_address")
        self.api_port = self.config.get("network").get("api_port")
        self.api_recv_port = self.config.get("network").get("api_recv_port")

        self.api = Api(self.api_address, self.api_port)
        self.api_recv = Api_recv(self.match, self.api_address, self.api_recv_port)
        self.info_api = Info_Api(self.match, self.match.robots, self.match.opposites, self.match.ball, self.match.coach_name)

    
    def start(self):
        self.app.start()

gui = GUI()
gui.start()
