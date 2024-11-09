
class Robot():
    def __init__(self, robot_id, robot_pos = [-5,-5,0], team = True):

        self.robot_id = robot_id
        self.robot_pos = robot_pos
        self.team = team
        self.strategy = None
        self.battery = None
        self.playing = False
        self.signal = None

    def change_team(self):
        if self.team:
            self.team = False
        else:
            self.team = True

    def update_information(self, info, team):
        """ Function to update values received in api """
        if str(self.robot_id) in info['ROBOT_POS'].keys():
            self. playing = True
            if str(self.robot_id) in info['ROBOT_POS']:
                self.robot_pos = info['ROBOT_POS'][str(self.robot_id)]
                if team:
                    if str(self.robot_id) in info['STRATEGY']:
                        self.strategy = info['STRATEGY'][str(self.robot_id)]
                    if str(self.robot_id) in info['BATTERY']:
                        self.battery = info['BATTERY'][str(self.robot_id)]
                    if str(self.robot_id) in info['SIGNAL']:
                        self.signal = info['SIGNAL'][str(self.robot_id)]
        else:
            self.playing = False