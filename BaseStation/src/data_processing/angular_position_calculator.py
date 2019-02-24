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
                next_x = i + self.sample_frequency
                self.x += self.trap_integrate(next_x, ang_vel_x[i+1], i, ang_vel_x[i])
                self.y += self.trap_integrate(next_x, ang_vel_y[i+1], i, ang_vel_y[i])
                self.z += self.trap_integrate(next_x, ang_vel_z[i+1], i, ang_vel_z[i])

        return self.x, self.y, self.z

    @staticmethod
    def trap_integrate(next_x: float, next_y: float, actual_x: float, actual_y: float):
        return (next_x - actual_x) * ((next_y + actual_y) * 0.5)
