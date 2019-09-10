class AngularCalculator:

    def __init__(self, sample_freq: float):
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0

        self.sample_frequency = sample_freq

    def __str__(self):
        return "roll({}), pitch({}), yaw({})".format(self.roll, self.pitch, self.yaw)

    def set_sampling_frequency(self, freq: float):
        self.sample_frequency = freq

    def integrate_all(self, ang_vel_x: list, ang_vel_y: list, ang_vel_z: list):
        total_len = len(ang_vel_x)
        if total_len == 0:
            return

        self.reset()

        actual_x = 0.0
        for i in range(total_len):
            if i < total_len-1:
                next_x = actual_x + 1.0 / self.sample_frequency
                self.roll += self.trap_integrate(next_x, ang_vel_x[i+1], actual_x, ang_vel_x[i])
                self.pitch += self.trap_integrate(next_x, ang_vel_y[i+1], actual_x, ang_vel_y[i])
                self.yaw += self.trap_integrate(next_x, ang_vel_z[i+1], actual_x, ang_vel_z[i])
                actual_x = next_x

        return self.roll, self.pitch, self.yaw

    @staticmethod
    def trap_integrate(next_x: float, next_y: float, actual_x: float, actual_y: float):
        return (next_x - actual_x) * ((next_y + actual_y) * 0.5)

    def get_last_angular_position(self):
        return self.roll, self.pitch, self.yaw

    def reset(self):
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
