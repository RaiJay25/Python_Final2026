# lander.py
from physics import euler_step, vertical_acceleration, horizontal_acceleration


class Lander:
    def __init__(self):
        self.x = 50.0
        self.y = 100.0
        self.vx = 0.0
        self.vy = 0.0

        self.width = 2.0
        self.height = 5.0

        self.thrust_power = 4.0
        self.move_power = 1.5

    def update(self, dt, thrust_on, move_left, move_right):
        ax = horizontal_acceleration(move_left, move_right, self.move_power)
        ay = vertical_acceleration(thrust_on, self.thrust_power)

        self.x, self.vx = euler_step(self.x, self.vx, ax, dt)
        self.y, self.vy = euler_step(self.y, self.vy, ay, dt)