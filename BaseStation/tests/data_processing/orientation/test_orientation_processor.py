from unittest import TestCase
from unittest.mock import Mock

from src.data_processing.orientation.angular_speed_integrator import AngularSpeedIntegrator
from src.data_processing.orientation.orientation import Orientation
from src.data_processing.orientation.orientation_initializer import OrientationInitializer
from src.data_processing.orientation.orientation_processor import OrientationProcessor
from tests.rocket_packet.rocket_packet_builder import RocketPacketBuilder


class OrientationProcessorTest(TestCase):
    INITIAL_TIMESTAMP = 5.0
    SUBSEQUENT_TIMESTAMP = 5.5
    INITIAL_ORIENTATION = Orientation(1, 2, 3)
    CURRENT_ORIENTATION = Orientation(4, 5, 6)
    ANGULAR_SPEED_X = 7
    ANGULAR_SPEED_Y = 8
    ANGULAR_SPEED_Z = 9

    def setUp(self):
        self.orientation_initializer = Mock(spec=OrientationInitializer)
        self.angular_speed_integrator = Mock(spec=AngularSpeedIntegrator)

        self.orientation_processor = OrientationProcessor(self.orientation_initializer, self.angular_speed_integrator)

    def test_update_should_update_orientation_initializer_when_initializing(self):
        rocket_packet = RocketPacketBuilder().build()

        self.orientation_processor.update(rocket_packet)

        self.orientation_initializer.update.assert_called_with(rocket_packet)

    def test_update_should_integrate_angular_speed_after_initialization(self):
        self.orientation_processor.notify_orientation_initialized(self.INITIAL_TIMESTAMP, self.INITIAL_ORIENTATION)
        rocket_packet = RocketPacketBuilder().with_timestamp(self.SUBSEQUENT_TIMESTAMP)\
            .with_angular_speed_x(self.ANGULAR_SPEED_X)\
            .with_angular_speed_y(self.ANGULAR_SPEED_Y)\
            .with_angular_speed_z(self.ANGULAR_SPEED_Z)\
            .build()

        self.orientation_processor.update(rocket_packet)

        self.angular_speed_integrator.integrate.assert_called_with(self.SUBSEQUENT_TIMESTAMP, self.ANGULAR_SPEED_X,
                                                                   self.ANGULAR_SPEED_Y, self.ANGULAR_SPEED_Z)

    def test_notify_orientation_initialized_should_set_initial_orientation(self):
        self.orientation_processor.notify_orientation_initialized(self.INITIAL_TIMESTAMP, self.INITIAL_ORIENTATION)

        self.angular_speed_integrator.set_initial_orientation.assert_called_with(self.INITIAL_TIMESTAMP,
                                                                                 self.INITIAL_ORIENTATION)

    def test_get_rocket_orientation_should_return_current_orientation(self):
        self.angular_speed_integrator.get_current_rocket_orientation.return_value = self.CURRENT_ORIENTATION

        orientation = self.orientation_processor.get_rocket_orientation()

        self.assertEqual(orientation, self.CURRENT_ORIENTATION)

    def test_reset_should_reset_orientation_initializer_and_angular_speed_calculator(self):
        self.orientation_processor.reset()

        self.orientation_initializer.reset.assert_called_with()
        self.angular_speed_integrator.reset.assert_called_with()
