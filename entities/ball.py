
class Ball():
    def __init__(self, ball_pos = (0,0)):
        
        self.ball_pos = ball_pos


    def update_information(self, info): #Function to update values recieved in api
        for key, value in info.items():
            setattr(self, key.lower(), value)        