
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
        data_send = self.match.gui_data
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

        