import math
import os
import time

from api import Api
import entities

CATEGORIES = {
    '3v3': 3, '5v5': 5
}

class Match():
    def __init__(self, team_side = "left", team_color = "blue", coach_name = None, category="3v3"):
        
        self.update_rate = 0
        self.coach_name = coach_name
        self.team_side =  team_side
        self.team_color = team_color
        self.category = category
        self.n_robots = CATEGORIES.get(self.category)

        self.opposite_team_color = 'yellow' if self.team_color == 'blue' else 'blue'

        self.game_status = 'STOP'

        self.ball = entities.Ball()
        self.robots = []
        self.opposites = []

        self.robots_ids = [5, 7, 8]
        self.opposites_ids = [0, 1, 2]

        # Default parameter values
        # TODO option to change default params/save them in a file
        self.control_parameters = {"kp":1, "ki":0, "kd":0, "kw":3.5, "rm":0.44, "vm":0.5}

        self.start()
        
    def start(self):
        self.opposites = [
            entities.Robot(i, [0,0,0], False) for i in self.opposites_ids
        ]

        self.robots = [
            entities.Robot(i, [0,0,0]) for i in self.robots_ids
        ]

    last_update_time: int = 0 #TODO: this solution is held with duct tape

    def update_information(self, **kwargs):
        """ Function to update values received in api """
        for key, value in kwargs.items():
            if hasattr(self, key.lower()):
                setattr(self, key.lower(), value)
        t_epoch = math.ceil(time.time() * 1000)
        self.update_rate = t_epoch - self.last_update_time
        self.last_update_time = t_epoch
    
    def set_game_status(self, status):
        self.game_status = status

    def set_team_color(self, color):
        if self.team_color != color:
            for robot in self.robots:
                 robot.change_team()
            for opposite in self.opposites:
                opposite.change_team()
            self.robots, self.opposites = self.opposites, self.robots
        self.team_color = color
        self.opposite_team_color = 'yellow' if self.team_color == 'blue' else 'blue'
    
    def set_team_side(self, side):
        self.team_side = side
    
    def set_control_parameters(self, parameters):
        self.control_parameters = parameters
    
    def fetch_robot_by_id(self, robot_id: int):
        # FIXME: cannot explicitly define Robot as function return type due to circular import
        for robot in self.robots:
            if robot.robot_id == robot_id: return robot
        return None
