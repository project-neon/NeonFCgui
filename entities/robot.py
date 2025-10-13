class Robot:
    def __init__(self, robot_id, robot_pos = [-5,-5,0], team = True):

        self.robot_id = robot_id
        self.robot_pos = robot_pos
        self.team = team
        self.strategy = None
        self.battery = None
        self.playing = False
        self.signal = None
        self.kicker = None  # TODO String? Check values

    def change_team(self):
        if self.team:
            self.team = False
        else:
            self.team = True

    def update_information(self, info, team=None):
        """ Function to update values received in api """
        self.robot_pos = (info.pos.x, info.pos.y, info.pos.z)

        # if str(self.robot_id) in info['ROBOT_POS'].keys():
        #     self.playing = True
        #     self.robot_pos = info.get('ROBOT_POS', {}).get(str(self.robot_id), self.robot_pos)
        #     if team:
        #             self.strategy = info.get('STRATEGY', {}).get(str(self.robot_id), self.strategy)
        #             self.battery = info.get('BATTERY', {}).get(str(self.robot_id), self.battery)
        #             self.signal = info.get('SIGNAL', {}).get(str(self.robot_id), self.signal)
        #             # self.kicker = info.get('KICKER', {}).get(str(self.robot_id), self.kicker)
        # else:
        #     self.playing = False
        #     self.robot_pos = (-5,-5,0)
