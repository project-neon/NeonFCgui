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
        self.battery = f"{info.battery}%"
        self.signal = info.rssi
