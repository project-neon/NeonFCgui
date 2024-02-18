import os
from api import Api
from entities import ball,robot

CATEGORIES = {
    '3v3': 3, '5v5': 5
}

class Match():
    def __init__(self, interface, team_side = "left", team_color = "blue", coach_name = None, category="3v3"):
        super().__init__()
        self.interface = interface # Interface instance
        
        self.coach_name = os.environ.get('COACH_NAME', coach_name) 
        self.team_side = os.environ.get('TEAM_SIDE', team_side) 
        self.team_color = os.environ.get('TEAM_COLOR', team_color)
        self.category = os.environ.get('CATEGORY', category)
        self.n_robots = CATEGORIES.get(self.category)

        self.opposite_team_color = 'yellow' if self.team_color == 'blue' else 'blue'

        self.game_status = 'STOP'

        self.ball = ball()
        self.robots = []
        self.opposites = []

        self.robots_ids = [5, 7, 8]
        self.opposites_ids = [0, 1, 2]

        self.start()
        
    def start(self):
        self.opposites = [
            robot(i, (0,0,0), False) for i in self.opposites_ids
        ]

        self.robots = [
            robot(i, (0,0,0)) for i in self.robots_ids
        ]


    def update_information(self, **kwargs): #Function to update values recieved in api
        for key, value in kwargs.items():
            if hasattr(self, key.lower()):
                setattr(self, key.lower(), value)

    
    def set_game_status(self, status):
        self.game_status = status
