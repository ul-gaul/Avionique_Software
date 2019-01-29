from math import *
from numpy import *

# Position en fonction de la vitesse. Integration numerique.
# Penser a intergrer pour les anciennes annees.
# Celon la vitesse angulaire, trouver les 3 angles en EULER

# https://physics.stackexchange.com/questions/73961/angular-velocity-expressed-via-euler-angles
# http://galileoandeinstein.physics.virginia.edu/7010/CM_26_Euler_Angles.html

# Formule: https://computergraphics.stackexchange.com/questions/8195/how-to-convert-euler-angles-to-quaternions-and-get-the-same-euler-angles-back-fr
# Spherical: https://www.omnicalculator.com/math/spherical-coordinates

# Avec les coordonees 50, 10, 2, on doit obtenir en angle: 51.03, 87.75, 11.31


class AngularCalculator:

    def __init__(self):
        self.angle = (0, 0, 0)
        self.quaternions = (0, 0, 0, 0)
        pass

    def compute_angular_velocity(self, ang_velocity: tuple):
        r = sqrt(pow(ang_velocity[0], 2) + pow(ang_velocity[1], 2) + pow(ang_velocity[2], 2))  # x
        teta = arccos(ang_velocity[2] / r)  # y
        phi = arctan(ang_velocity[1] / ang_velocity[0])  # z

        self.angle = r, teta, phi
        self.euler_to_quaternion(phi, teta, r)  # Z Y X

    def euler_to_quaternion(self, roll, pitch, yaw):
        # roll = radians(roll)
        # pitch = radians(roll)
        # yaw = radians(roll)
        #
        # qx = sin(roll * 0.5) * cos(pitch * 0.5) * cos(yaw * 0.5) - cos(roll * 0.5) * sin(pitch * 0.5) * sin(yaw * 0.5)
        # qy = cos(roll * 0.5) * sin(pitch * 0.5) * cos(yaw * 0.5) + sin(roll * 0.5) * cos(pitch * 0.5) * sin(yaw * 0.5)
        # qz = cos(roll * 0.5) * cos(pitch * 0.5) * sin(yaw * 0.5) - sin(roll * 0.5) * sin(pitch * 0.5) * cos(yaw * 0.5)
        # qw = cos(roll * 0.5) * cos(pitch * 0.5) * cos(yaw * 0.5) + sin(roll * 0.5) * sin(pitch * 0.5) * sin(yaw * 0.5)

        # cy = cos(yaw * 0.5)
        # sy = sin(yaw * 0.5)
        # cp = cos(pitch * 0.5)
        # sp = sin(pitch * 0.5)
        # cr = cos(roll * 0.5)
        # sr = sin(roll * 0.5)

        c1 = cos(yaw * 0.5)
        s1 = sin(yaw * 0.5)
        c2 = cos(pitch * 0.5)
        s2 = sin(pitch * 0.5)
        c3 = cos(roll * 0.5)
        s3 = sin(roll * 0.5)

        c1c2 = c1 * c2
        s1s2 = s1 * s2

        qw = c1c2 * c3 - s1s2 * s3
        qx = c1c2 * s3 + s1s2 * c3
        qy = s1 * c2 * c3 + c1 * s2 * s3
        qz = c1 * s2 * c3 - s1 * c2 * s3

        # qw = cy * cp * cr + sy * sp * sr
        # qx = cy * cp * sr - sy * sp * cr
        # qy = sy * cp * sr + cy * sp * cr
        # qz = sy * cp * cr - cy * sp * sr

        self.quaternions = qx, qy, qz, qw

    def get_angles_degrees(self):
        return degrees(self.angle[0]), degrees(self.angle[1]), degrees(self.angle[2])

    def get_angles_radians(self):
        return self.angle

    def get_quaternions(self):
        return self.quaternions
