from unittest import TestCase
from unittest.mock import Mock

from src.data_processing.gps.gps_initializer import GpsInitializer, GpsInitializerListener
from src.data_processing.gps.utm_coordinates import UTMCoordinates


class GpsInitializerTest(TestCase):
    INITIALIZATION_DELAY_IN_SECONDS = 2
    NO_INITIALIZATION_DELAY = 0
    INITIAL_COORDINATES = UTMCoordinates(1234, 2345)
    NOISE = UTMCoordinates(0.1, 0.2)

    def setUp(self):
        self.gps_initializer = GpsInitializer(self.INITIALIZATION_DELAY_IN_SECONDS)

        self.gps_initializer_listener = Mock(spec=GpsInitializerListener)
        self.gps_initializer.register_listener(self.gps_initializer_listener)

    def test_update_should_not_notify_listeners_before_delay(self):
        self.gps_initializer.update(0, self.INITIAL_COORDINATES)

        self.gps_initializer.update(1, self.INITIAL_COORDINATES + self.NOISE)

        self.gps_initializer_listener.notify_initialization_complete.assert_not_called()

    def test_update_should_notify_listeners_with_average_base_camp_position_after_delay(self):
        self.gps_initializer.update(0, self.INITIAL_COORDINATES)
        self.gps_initializer.update(1, self.INITIAL_COORDINATES + self.NOISE)

        self.gps_initializer.update(3, self.INITIAL_COORDINATES - self.NOISE)

        self.gps_initializer_listener.notify_initialization_complete.assert_called_with(self.INITIAL_COORDINATES)

    def test_update_should_notify_listeners_when_elapsed_time_equals_delay(self):
        self.gps_initializer.update(0, UTMCoordinates(1.0, 5.0))
        self.gps_initializer.update(1, UTMCoordinates(1.5, 7.0))

        self.gps_initializer.update(2, UTMCoordinates(6.5, 9.0))

        self.gps_initializer_listener.notify_initialization_complete.assert_called_with(UTMCoordinates(3.0, 7.0))

    def test_update_should_notify_listeners_given_no_delay(self):
        self.gps_initializer.initialization_delay = 0

        self.gps_initializer.update(0, self.INITIAL_COORDINATES)

        self.gps_initializer_listener.notify_initialization_complete.assert_called_with(self.INITIAL_COORDINATES)
