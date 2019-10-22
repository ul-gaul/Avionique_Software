import abc

import math

from src.data_processing.orientation.orientation import Orientation
from src.rocket_packet.rocket_packet import RocketPacket


class OrientationInitializerListener:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def notify_orientation_initialized(self, timestamp: float, orientation: Orientation):
        pass


# TODO: finish this algorithm and test it
class OrientationInitializer:
    def __init__(self, initialization_delay_in_seconds: float):
        self.initialization_delay = initialization_delay_in_seconds
        self.listeners = []
        self._first_timestamp = None
        self._initialisation_roll = []
        self._initialisation_pitch = []
        self._initialisation_yaw = []

    def register_listener(self, listener: OrientationInitializerListener):
        self.listeners.append(listener)

    def update(self, rocket_packet: RocketPacket):
        self._accumulate_data(rocket_packet)

        elapsed_time = self._get_elapsed_time_since_first_timestamp(rocket_packet.time_stamp)
        if elapsed_time >= self.initialization_delay:
            initial_orientation = self._measure_initial_orientation()
            self._notify_listeners(rocket_packet.time_stamp, initial_orientation)

    def reset(self):
        self._first_timestamp = None
        self._initialisation_roll = []
        self._initialisation_pitch = []
        self._initialisation_yaw = []

    def _get_elapsed_time_since_first_timestamp(self, timestamp: float):
        if self._first_timestamp is None:
            self._first_timestamp = timestamp
            return 0
        else:
            return timestamp - self._first_timestamp

    def _notify_listeners(self, timestamp: float, orientation: Orientation):
        for listener in self.listeners:
            listener.notify_orientation_initialized(timestamp, orientation)

    def _accumulate_data(self, rocket_packet: RocketPacket):
        spherical_coordinates = self._to_spherical(rocket_packet.acceleration_x, rocket_packet.acceleration_y,
                                                   rocket_packet.acceleration_z)
        self._initialisation_roll.append(math.degrees(math.sin(spherical_coordinates[1]) * spherical_coordinates[2]))
        self._initialisation_pitch.append(math.degrees(math.cos(spherical_coordinates[1]) * spherical_coordinates[2]))
        self._initialisation_yaw.append(0)

    def _to_spherical(self, accel_x, accel_y, accel_z):
        spherical = [0, 0, 0]

        spherical[0] = self._norm(accel_x, accel_y, accel_z)
        spherical[1] = math.atan2(accel_y, accel_x)
        spherical[2] = math.acos(accel_z / spherical[0])
        return spherical

    def _norm(self, x, y, z):
        return math.sqrt(x ** 2 + y ** 2 + z ** 2)

    def _measure_initial_orientation(self):
        roll = self._average(self._initialisation_roll)
        pitch = self._average(self._initialisation_pitch)
        yaw = self._average(self._initialisation_yaw)

        return Orientation(0, 0, 0)

    def _average(self, data: list):
        return sum(data) / len(data)
