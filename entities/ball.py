
class Ball():
    def __init__(self, ball_pos = (0,0)):
        
        self.ball_pos = ball_pos


    def update_information(self, info): #Function to update values recieved in api
        if 'BALL_POS' in info:
            self.ball_pos = info['BALL_POS']