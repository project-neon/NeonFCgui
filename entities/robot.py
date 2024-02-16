
class Robot():
    def __init__(self, robot_pos = (0,0,0)):

        self.robot_pos = robot_pos


    def update_information(self, **kwargs): #Function to update values recieved in api
        for key, value in kwargs.items():
            if hasattr(self, key.lower()):
                setattr(self, key.lower(), value)   