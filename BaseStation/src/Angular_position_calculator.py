from math import *
from numpy import *
# from numpy import Quaternion
# Position en fonction de la vitesse. Integration numerique.
# Penser a intergrer pour les anciennes annees.
# Celon la vitesse angulaire, trouver les 3 angles en EULER

# https://physics.stackexchange.com/questions/73961/angular-velocity-expressed-via-euler-angles
# http://galileoandeinstein.physics.virginia.edu/7010/CM_26_Euler_Angles.html

# Avec les coordonees 50, 10, 2, on doit obtenir en angle: 51.03, 87.75, 11.31

class AngularCalculator:

    def __init__(self):
        self.prev_ang_velocity = None
        pass

    def compute_angular_velocity(self, quats: tuple):
        if len(quats) > 0:
            print(quats[0], quats[1], quats[2], quats[3])

    def compute_angular_position(self, ang_velocity: tuple):
        r = sqrt(pow(ang_velocity[0], 2) + pow(ang_velocity[1], 2) + pow(ang_velocity[2], 2))
        teta = degrees(arccos(ang_velocity[2] / r))
        phi = degrees(arctan(ang_velocity[1] / ang_velocity[0]))

        return r, teta, phi


    def get_angular_velocity(self):
        return self.angular_velocity

    def get_angular_position(self):
        return self.angular_position
