import abc
from typing import List

from src.data_processing.gps.utm_coordinates import UTMCoordinates


class GpsInitializerListener:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def notify_initialization_complete(self, base_camp_coordinates: UTMCoordinates):
        pass


class GpsInitializer:

    def __init__(self, initialization_delay_in_seconds: float):
        self.initialization_delay = initialization_delay_in_seconds
        self.listeners = []
        self._first_timestamp = None
        self._initialization_coordinates = []

    def register_listener(self, listener: GpsInitializerListener):
        self.listeners.append(listener)

    def update(self, timestamp: float, utm_coordinates: UTMCoordinates):
        self._initialization_coordinates.append(utm_coordinates)

        elapsed_time = self._get_elapsed_time_since_first_timestamp(timestamp)
        if elapsed_time >= self.initialization_delay:
            base_camp_coordinates = self._average(self._initialization_coordinates)

            self._notify_listeners(base_camp_coordinates)

    def reset(self):
        self._first_timestamp = None
        self._initialization_coordinates = []

    def _get_elapsed_time_since_first_timestamp(self, timestamp: float):
        if self._first_timestamp is None:
            self._first_timestamp = timestamp
            return 0
        else:
            return timestamp - self._first_timestamp

    @staticmethod
    def _average(initialization_coordinates: List[UTMCoordinates]):
        return sum(initialization_coordinates, UTMCoordinates(0.0, 0.0)) / len(initialization_coordinates)

    def _notify_listeners(self, base_camp_coordinates: UTMCoordinates):
        for listener in self.listeners:
            listener.notify_initialization_complete(base_camp_coordinates)
