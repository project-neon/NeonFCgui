
class InfoApi():
    update_list = []

    def __init__(self, match, robots, opposites, ball, parameters, coach = None):
        
        self.match = match
        self.robots = robots
        self.opposites = opposites
        self.coach = coach
        self.ball = ball
        self.parameters = parameters

        self.data = {}


    def organize_send(self):
        data_dict = dict(
            {
                "MATCH": {
                    "GAME_STATUS": self.match.game_status,
                    "TEAM_SIDE": self.match.team_side,
                    "TEAM_COLOR": self.match.team_color,
                    "GOALKEEPER_ID": self.match.gk_id
                },
                "FOULS": {
                    "FOUL_NAME": self.match.current_foul,
                    "FOUL_QUADRANT": self.match.foul_quadrant,
                    "FOUL_COLOR": self.match.foul_color,
                    "FOUL_IS_ACTIVE": self.match.foul_is_active
                },
            }
        )

        self.save_data(data_dict)

        return data_dict

    def update_recv(self,info_recv):

        self.match.update_information(info_recv) #'FIELD_SIZE': [size.x, size.y]

        if 'BALL' in info_recv:
            self.ball.update_information(info_recv['BALL'])


        if 'TEAM_ROBOTS' in info_recv:
                for robot in self.robots:
                    robot.update_information(info_recv['TEAM_ROBOTS'], True)

        if 'OPPOSITE_ROBOTS' in info_recv:
            for opposite in self.opposites:
                opposite.update_information(info_recv['OPPOSITE_ROBOTS'], False)

        self.save_data(info_recv)

    def save_data(self,info_save):

        for i in info_save:
            self.data.update({i: info_save[i]})

        