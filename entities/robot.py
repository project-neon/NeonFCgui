
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

    def update_information(self, info):
        """ Function to update values received in api """
        self.robot_pos = info['ROBOT_POS'][str(self.robot_id)]
        if self.team:   
            self.strategy = info['STRATEGY'][str(self.robot_id)]