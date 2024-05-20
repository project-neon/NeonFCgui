
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

        self.parameters = self.match.control_parameters

        data_send = dict(
        {'MATCH':
            {'TEAM_COLOR' :  self.match.team_color,
             'GAME_STATUS' : self.match.game_status,
             'TEAM_SIDE' : self.match.team_side,
             'COACH_NAME': self.match.coach_name
            },
         'PARAMETERS': 
            {'PID_KP': self.parameters['pid_kp'],
             'KI': self.parameters['ki'],
             'KD': self.parameters['kd'],
             'KW': self.parameters['kw'],
             'VM': self.parameters['vm'],
             'RM': self.parameters['rm'],
             'UNI_KP': self.parameters['uni_kp']
            }
        })

        #print(data_send)

        self.save_data(data_send)

        return data_send

    def update_recv(self,info_recv):
        
        self.match.update_information(info_recv['MATCH'])
        self.ball.update_information(info_recv['BALL'])
        for robot in self.robots:
            robot.update_information(info_recv['TEAM_ROBOTS'])

        for opposite in self.opposites:
            opposite.update_information(info_recv['OPPOSITE_ROBOTS'])

        self.save_data(info_recv)

    def save_data(self,info_save):

        for i in info_save:
            self.data.update({i: info_save[i]})

        