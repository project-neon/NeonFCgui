class AnimationManager:
    dest: float = 0
    current: float = 0
    vel: float = 0

    accel_constant: float = .03
    vel_constant: float = .8
    anti_derivative_constant: float = .05

    def __init__(self, accel_constant=.03, vel_constant=.8, anti_derivative_constant=.05):
        self.accel_constant = accel_constant
        self.vel_constant = vel_constant
        self.anti_derivative_constant = anti_derivative_constant

    def update(self, time: float):
        error = self.dest - self.current
        self.vel += error * self.accel_constant * time * self.anti_derivative_constant
        self.vel -= self.vel * self.anti_derivative_constant
        self.current += self.vel * time * self.vel_constant

    def set_dest(self, dest: float):
        self.dest = dest
