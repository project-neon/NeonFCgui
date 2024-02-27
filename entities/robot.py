
class Robot():
    def __init__(self, robot_id, robot_pos = [0,0,0], team = True):

        self.robot_id = robot_id
        self.robot_pos = robot_pos
        self.team = team
        self.strategy = None


    def change_team(self):
        if self.team:
            self.team = False
        else:
            self.team = True

    def update_information(self, **kwargs):
        """ Function to update values received in api """
        for key, value in kwargs.items():
            if key == 'TEAM_ROBOTS_POS' and self.team == True:
                for pos in value:
                    self.robot_pos = pos.get(str(self.robot_id), self.robot_pos)
            elif key == 'OPPOSITE_ROBOTS_POS' and self.team == False:
                for pos in value:
                    self.robot_pos = pos.get(str(self.robot_id), self.robot_pos)
            elif key == 'ROBOTS_STRATEGY' and self.team == True:
                for strat in value:     
                    self.strategy = strat.get(str(self.robot_id), self.strategy)