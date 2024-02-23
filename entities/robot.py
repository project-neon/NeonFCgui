
class Robot():
    def __init__(self, robot_id, robot_pos = (0,0,0), team = True):

        self.robot_id = robot_id
        self.robot_pos = robot_pos
        self.team = team
        self.strategy = None


    def update_information(self, **kwargs):
        """ Function to update values received in api """
        for key, value in kwargs.items():
            if key == 'TEAM_ROBOTS_POS' and self.team == True:
                self.robot_pos = value.get(self.robot_id)
            elif key == 'OPPOSITE_ROBOTS_POS' and self.team == False:
                self.robot_pos = value.get(self.robot_id)
            elif key == 'ROBOTS_STRATEGY' and self.team == True:
                self.strategy = value.get(self.robot_id)