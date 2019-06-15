class AngularCalculator:

    def __init__(self):
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0

    def __str__(self):
        return "roll({}), pitch({}), yaw({})".format(self.roll, self.pitch, self.yaw)

    def integrate_all(self, time_stamp: list, ang_vel_x: list, ang_vel_y: list, ang_vel_z: list):
        self.reset()

        total_len = len(time_stamp)
        if total_len == 0:
            return

        current_time = time_stamp[0]
        for i in range(total_len):
            if i < total_len-1:
                next_time = time_stamp[i+1]
                self.roll += self.trap_integrate(next_time, ang_vel_x[i+1], current_time, ang_vel_x[i])
                self.pitch += self.trap_integrate(next_time, ang_vel_y[i+1], current_time, ang_vel_y[i])
                self.yaw += self.trap_integrate(next_time, ang_vel_z[i+1], current_time, ang_vel_z[i])
                current_time = next_time

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
