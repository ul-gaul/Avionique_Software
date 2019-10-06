import math

from src.data_processing.angular_speed_integrator import AngularSpeedIntegrator
from src.data_processing.quaternion import Quaternion
from src.rocket_packet.rocket_packet import RocketPacket


class OrientationProcessor:
    def __init__(self, initialisation_delay_in_seconds: float, angular_speed_integrator: AngularSpeedIntegrator):
        self._initialisation_delay = initialisation_delay_in_seconds
        self._angular_speed_integrator = angular_speed_integrator
        self._initialisation_roll = []
        self._initialisation_pitch = []
        self._initialisation_yaw = []
        self._first_timestamp = None
        self._initialising = True

    def update(self, rocket_packet: RocketPacket):
        elapsed_time = self._get_elapsed_time_since_first_packet(rocket_packet)

        if self._initialising and elapsed_time >= self._initialisation_delay:
            roll = self.average(self._initialisation_roll)
            pitch = self.average(self._initialisation_pitch)
            yaw = self.average(self._initialisation_yaw)
            # FIXME: instantiate a new object, potentially with a factory
            self._angular_speed_integrator.set_initial_orientation(rocket_packet.time_stamp, roll, pitch, yaw)
            self._initialising = False

        if elapsed_time < self._initialisation_delay:
            spherical_coordinates = self.to_spherical(rocket_packet.acceleration_x, rocket_packet.acceleration_y,
                                                      rocket_packet.acceleration_z)
            self._initialisation_roll.append(math.degrees(math.sin(spherical_coordinates[1]) * spherical_coordinates[2]))
            self._initialisation_pitch.append(math.degrees(math.cos(spherical_coordinates[1]) * spherical_coordinates[2]))
            self._initialisation_yaw.append(0)
            self._initialising = True
        else:
            self._angular_speed_integrator.integrate(rocket_packet.time_stamp, rocket_packet.angular_speed_x,
                                                     rocket_packet.angular_speed_y, rocket_packet.angular_speed_z)
            self._initialising = False

    def _get_elapsed_time_since_first_packet(self, rocket_packet: RocketPacket):
        if self._first_timestamp is None:
            self._first_timestamp = rocket_packet.time_stamp
            return 0
        else:
            return rocket_packet.time_stamp - self._first_timestamp

    def get_rocket_rotation(self):
        euler_angles = self._angular_speed_integrator.get_current_rocket_orientation()
        return Quaternion.euler_degrees_to_quaternion(euler_angles[2], euler_angles[1], euler_angles[0])

    def reset(self):
        self._initialisation_roll = []
        self._initialisation_pitch = []
        self._initialisation_yaw = []
        self._first_timestamp = None
        self._initialising = True
        self._angular_speed_integrator.reset()

    def to_spherical(self, accel_x, accel_y, accel_z):
        spherical = [0, 0, 0]

        spherical[0] = self.norm(accel_x, accel_y, accel_z)
        spherical[1] = math.atan2(accel_y, accel_x)
        spherical[2] = math.acos(accel_z / spherical[0])
        return spherical

    def norm(self, x, y, z):
        return math.sqrt(x ** 2 + y ** 2 + z ** 2)

    def average(self, data: list):
        return sum(data) / len(data)
