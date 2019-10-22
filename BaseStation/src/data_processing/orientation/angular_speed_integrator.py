from src.data_processing.orientation.orientation import Orientation


class AngularSpeedIntegrator:
    def __init__(self):
        self.last_time = 0
        self.last_angular_speed_x = 0
        self.last_angular_speed_y = 0
        self.last_angular_speed_z = 0
        self.roll = 0
        self.pitch = 0
        self.yaw = 0

    def set_initial_orientation(self, initial_time: float, initial_orientation: Orientation):
        self.last_time = initial_time
        self.roll = initial_orientation.roll
        self.pitch = initial_orientation.pitch
        self.yaw = initial_orientation.yaw

    def integrate(self, current_time: float, angular_speed_x: float, angular_speed_y: float, angular_speed_z: float):
        self.roll += self.trap_integrate(current_time, angular_speed_x, self.last_time, self.last_angular_speed_x)
        self.pitch += self.trap_integrate(current_time, angular_speed_y, self.last_time, self.last_angular_speed_y)
        self.yaw += self.trap_integrate(current_time, angular_speed_z, self.last_time, self.last_angular_speed_z)

        self.last_time = current_time
        self.update_last_angular_speed(angular_speed_x, angular_speed_y, angular_speed_z)

    def get_current_rocket_orientation(self) -> Orientation:
        return Orientation(self.roll, self.pitch, self.yaw)

    def reset(self):
        self.last_time = 0
        self.last_angular_speed_x = 0
        self.last_angular_speed_y = 0
        self.last_angular_speed_z = 0
        self.roll = 0
        self.pitch = 0
        self.yaw = 0

    @staticmethod
    def trap_integrate(next_x: float, next_y: float, actual_x: float, actual_y: float):
        return (next_x - actual_x) * ((next_y + actual_y) * 0.5)

    def update_last_angular_speed(self, angular_speed_x: float, angular_speed_y: float, angular_speed_z: float):
        self.last_angular_speed_x = angular_speed_x
        self.last_angular_speed_y = angular_speed_y
        self.last_angular_speed_z = angular_speed_z
