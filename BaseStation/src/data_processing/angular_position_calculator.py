from numpy import arccos, arctan, sqrt, radians, degrees

# ang_velocity sont des rads.
# Faire l inegral de la vitesse [ang_velocity].
# Transformer la position en quaternion.
# 1 class qui fait l integral.
# 1 class qui fait la conversion en quaternion. DONE
# Pas de position initiales ! [On la determine de base (0, 0, 0)].
# Cree une class quaternion pour eviter les confusions de W X Y Z => Cree des methodes static de conversion.

# Revoir les tests unitaires car toute les methodes, et verifcations ont ete change. DONE

# Demander a Maxime si l integrale on doit la calculer depuis le debut.
# Cela eviterais des bug sur le rewind.
# Plus de precision sur l inegration numerique.


class AngularCalculator:

    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

        self.sample_frequency = 1.0

    def __str__(self):
        return "x({}), y({}), z({})".format(self.x, self.y, self.z)

    def set_sampling_frequency(self, freq: float):
        self.sample_frequency = freq

    def integrate_all(self, ang_vel_x: list, ang_vel_y: list, ang_vel_z: list):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

        total_len = len(ang_vel_x)
        if total_len == 0:
            return

        for i in range(total_len):
            if i < total_len-1:
                self.x += self.trap_integrate(i+1, ang_vel_x[i+1], i, ang_vel_x[i])
                self.y += self.trap_integrate(i+1, ang_vel_y[i+1], i, ang_vel_y[i])
                self.z += self.trap_integrate(i+1, ang_vel_z[i+1], i, ang_vel_z[i])

    @staticmethod
    def trap_integrate(next_x: float, next_y: float, actual_x: float, actual_y: float):
        return (next_x - actual_x) * ((next_y + actual_y) * 0.5)
