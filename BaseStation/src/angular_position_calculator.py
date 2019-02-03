from numpy import arccos, arctan, sqrt, radians, degrees, cos, sin


class AngularCalculator:

    def __init__(self):
        self.angles = (0, 0, 0)
        self.quaternions = (0, 0, 0, 0)

    def compute_angular_velocity(self, ang_velocity: tuple):
        theta = 0
        psi = 0

        r = sqrt(pow(ang_velocity[0], 2) + pow(ang_velocity[1], 2) + pow(ang_velocity[2], 2))  # x

        if r != 0:
            theta = arccos(ang_velocity[2] / r)  # y
        if ang_velocity[0] != 0:
            psi = arctan(ang_velocity[1] / ang_velocity[0])  # z

        self.angles = radians(r), theta, psi
        self.euler_radians_to_quaternion(self.angles[2], self.angles[1], self.angles[0])

    def euler_radians_to_quaternion(self, yaw, pitch, roll):  # Z Y X
        cy = cos(yaw * 0.5)
        sy = sin(yaw * 0.5)
        cp = cos(pitch * 0.5)
        sp = sin(pitch * 0.5)
        cr = cos(roll * 0.5)
        sr = sin(roll * 0.5)

        qw = cy * cp * cr + sy * sp * sr
        qx = cy * cp * sr - sy * sp * cr
        qy = sy * cp * sr + cy * sp * cr
        qz = sy * cp * cr - cy * sp * sr

        self.quaternions = qx, qy, qz, qw

    def euler_degrees_to_quaternion(self, yaw, pitch, roll):  # Z Y X
        cy = cos(radians(yaw) * 0.5)
        sy = sin(radians(yaw) * 0.5)
        cp = cos(radians(pitch) * 0.5)
        sp = sin(radians(pitch) * 0.5)
        cr = cos(radians(roll) * 0.5)
        sr = sin(radians(roll) * 0.5)

        qw = cy * cp * cr + sy * sp * sr
        qx = cy * cp * sr - sy * sp * cr
        qy = sy * cp * sr + cy * sp * cr
        qz = sy * cp * cr - cy * sp * sr

        self.quaternions = qx, qy, qz, qw

    def get_angles_degrees(self):
        return degrees(self.angles[0]), degrees(self.angles[1]), degrees(self.angles[2])

    def get_angles_radians(self):
        return self.angles

    def get_quaternions(self):
        return self.quaternions
