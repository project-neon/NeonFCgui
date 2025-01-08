
class Ball():
    def __init__(self, ball_pos = (0,0)):
        
        self.ball_pos = ball_pos


    def update_information(self, info): #Function to update values recieved in api
            self.ball_pos = info.get('BALL_POS', self.ball_pos)