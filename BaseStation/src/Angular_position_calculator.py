#from numpy import Quaternion


class AngularCalculator:

    def __init__(self):
        self.angular_velocity = None
        self.angular_position = None
        pass

    def compute_angular_velocity(self, quats: tuple):
        if len(quats) > 0:
            print(quats[0], quats[1], quats[2], quats[3])
            self.angular_velocity = 0, 0, 0

    def compute_angular_position(self, ang_velocity: tuple):
        self.angular_position = 0, 0, 0

    def get_angular_velocity(self):
        return self.angular_velocity

    def get_angular_position(self):
        return self.angular_position
