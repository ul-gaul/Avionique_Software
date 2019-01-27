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
        r = sqrt(pow(ang_velocity[0], 2) + pow(ang_velocity[1], 2) + pow(ang_velocity[2], 2))
        teta = degrees(arccos(ang_velocity[2] / r))
        phi = degrees(arctan(ang_velocity[1] / ang_velocity[0]))

        self.angle = r, teta, phi
        self.euler_to_quaternion(teta, phi, r)

    def euler_to_quaternion(self, roll, pitch, yaw):
        qx = sin(roll * 0.5) * cos(pitch * 0.5) * cos(yaw * 0.5) - cos(roll * 0.5) * sin(pitch * 0.5) * sin(yaw * 0.5)
        qy = cos(roll * 0.5) * sin(pitch * 0.5) * cos(yaw * 0.5) + sin(roll * 0.5) * cos(pitch * 0.5) * sin(yaw * 0.5)
        qz = cos(roll * 0.5) * cos(pitch * 0.5) * sin(yaw * 0.5) - sin(roll * 0.5) * sin(pitch * 0.5) * cos(yaw * 0.5)
        qw = cos(roll * 0.5) * cos(pitch * 0.5) * cos(yaw * 0.5) + sin(roll * 0.5) * sin(pitch * 0.5) * sin(yaw * 0.5)

        self.quaternions = qx, qy, qz, qw

    def get_angles(self):
        return self.angle

    def get_quaternions(self):
        return self.quaternions
