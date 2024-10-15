import math
import os
import time
import json
from api import Api
import entities
from entities import robot

CATEGORIES = {
    'MINI': 3, 'SSL': 6
}
# TODO change categories

class Match():
    def __init__(self, team_side = "left", team_color = "blue", coach_name = 'No coach found', category="MINI"):
        
        self.update_rate = 0
        self.coach_name = coach_name
        self.coach_list = ['No coach found']
        self.team_side =  team_side
        self.team_color = team_color

        self.category = category
        self.n_robots = CATEGORIES.get(self.category)

        self.opposite_team_color = 'yellow' if self.team_color == 'blue' else 'blue'

        self.game_status = 'STOP'
        self.foul_quadrant = 1
        self.foul_color = 'blue'
        self.current_foul = ''
        self.foul_is_active = False

        self.ball = entities.Ball()
        self.robots = []
        self.opposites = []

        self.robots_ids = [5, 7, 8]
        self.opposites_ids = [1, 2, 3] # Placeholders so they don't override the robot_id values at the field_view

        # Default parameter values
        # TODO option to change default params/save them in a file
        self.control_parameters = {"pid_kp":1, "ki":0, "kd":0, "kw":3.5, "rm":0.44, "vm":0.5, "uni_kp":1}

        # Modo da interface: "Treino" ou "Competição"
        self.gui_mode = "Treino"

        self.start()
        
    def start(self):
        self.opposites = [
            entities.Robot(i, [0,0,0], False) for i in self.opposites_ids
        ]

        self.robots = [
            entities.Robot(i, [0,0,0]) for i in self.robots_ids
        ]

        self.update_info_json_file()

    last_update_time: int = 0

    def update_information(self, info):
        """ Function to update values received in api """
        for key, value in info.items():
            setattr(self, key.lower(), value)
        t_epoch = math.ceil(time.time() * 1000)
        self.update_rate = t_epoch - self.last_update_time
        self.last_update_time = t_epoch
        self.update_info_json_file()
    
    def set_game_status(self, status):
        self.game_status = status
        if status == "GAME_ON" or status == "STOP" or status == "HALT":
            self.foul_is_active = False
        self.update_info_json_file()
    
    def set_foul_quadrant(self, q):
        self.foul_quadrant = q
        self.update_info_json_file()
    
    def set_foul_color(self, c):
        self.foul_color = c
        self.update_info_json_file()
    
    def set_current_foul(self, f):
        self.current_foul = f
        self.foul_is_active = True
        self.update_info_json_file()

    def set_team_color(self, color):
        if self.team_color != color:
            for robot in self.robots:
                 robot.change_team()
            for opposite in self.opposites:
                opposite.change_team()
            self.robots, self.opposites = self.opposites, self.robots
        self.team_color = color
        self.opposite_team_color = 'yellow' if self.team_color == 'blue' else 'blue'
        self.update_info_json_file()
    
    def set_team_side(self, side):
        self.team_side = side
        self.update_info_json_file()
    
    def set_control_parameters(self, parameters):
        self.control_parameters = parameters
        self.update_info_json_file()
    
    def fetch_robot_by_id(self, robot_id: int):
        # FIXME: cannot explicitly define Robot as function return type due to circular import
        for robot in self.robots:
            if robot.robot_id == robot_id: return robot
        return None
    
    def set_category(self, cat):
        self.category = cat
        self.update_info_json_file()
    
    def update_info_json_file(self):
        self.gui_data = dict(
            {
                "MATCH": {
                    "GAME_STATUS": self.game_status,
                    "TEAM_SIDE": self.team_side,
                    "TEAM_COLOR": self.team_color,
                    "COACH_NAME": self.coach_name,
                    "CATEGORY": self.category,
                    "ROBOT_IDS": self.robots_ids,
                    "OPPOSITE_IDS": self.opposites_ids,
                    "UPDATE_RATE": self.update_rate,
                    "COACH_LIST": self.coach_list
                },
                'PARAMETERS': {
                    'PID_KP': self.control_parameters['pid_kp'],
                    'KI': self.control_parameters['ki'],
                    'KD': self.control_parameters['kd'],
                    'KW': self.control_parameters['kw'],
                    'VM': self.control_parameters['vm'],
                    'RM': self.control_parameters['rm'],
                    'UNI_KP': self.control_parameters['uni_kp']
                },
                "FOULS": {
                    "FOUL_NAME": self.current_foul,
                    "FOUL_QUADRANT": self.foul_quadrant,
                    "FOUL_COLOR": self.foul_color,
                    "FOUL_IS_ACTIVE": self.foul_is_active
                },
                "GUI_MODE": self.gui_mode
            }
        )
        # update gui_info.json
        # with open('files/gui_info.json', 'w') as f:
        #     json.dump(self.gui_data, f)
        with open('files/gui_info.json', 'w', encoding='utf-8') as f:
            json.dump(self.gui_data, f, ensure_ascii=False, indent=4)
