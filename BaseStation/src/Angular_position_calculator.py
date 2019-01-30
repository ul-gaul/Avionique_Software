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
        self.angles = (0, 0, 0)
        self.quaternions = (0, 0, 0, 0)
        pass

    def compute_angular_velocity(self, ang_velocity: tuple):
        r = sqrt(pow(ang_velocity[0], 2) + pow(ang_velocity[1], 2) + pow(ang_velocity[2], 2))  # x
        theta = arccos(ang_velocity[2] / r)  # y
        psi = arctan(ang_velocity[1] / ang_velocity[0])  # z

        self.angles = r, theta, psi
        self.euler_to_quaternion(degrees(psi), degrees(theta), r)  # XYZ

    def euler_to_quaternion(self, bank, heading, attitude):
        c1 = cos(heading * 0.5)
        c2 = cos(attitude * 0.5)
        c3 = cos(bank * 0.5)
        s1 = sin(heading * 0.5)
        s2 = sin(attitude * 0.5)
        s3 = sin(bank * 0.5)

        qw = c1*c2*c3 + s1*s2*s3
        qx = c1*c2*s3 - s1*s2*c3
        qy = c1*s2*c3 + s1*c2*s3
        qz = s1*c2*c3 - c1*s2*s3

        self.quaternions = qx, qy, qz, qw

    def get_angles_degrees(self):
        return self.angles[0], degrees(self.angles[1]), degrees(self.angles[2])

    def get_angles_radians(self):
        return self.angles

    def get_quaternions(self):
        return self.quaternions
