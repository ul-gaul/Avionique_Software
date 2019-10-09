import unittest
from unittest.mock import Mock, MagicMock, call, patch

from src.controller import Controller
from src.data_processing.consumer import Consumer
from src.data_processing.consumer_factory import ConsumerFactory
from src.data_processing.gps.gps_coordinates import GpsCoordinates
from src.data_processing.orientation.orientation import Orientation
from src.data_producer import DataProducer
from src.message_listener import MessageListener
from src.message_type import MessageType
from src.openrocket_simulation import InvalidOpenRocketSimulationFileException
from src.ui.data_widget import DataWidget
from tests.builders.config_builder import ConfigBuilder
from tests.matchers import AnyStringWith


class ControllerTest(unittest.TestCase):

    TIMESTAMPS = [1]
    ALTITUDES = [9000]
    APOGEE = 10000
    EASTINGS = [32]
    NORTHINGS = [52]
    GPS_COORDINATES = GpsCoordinates(46.77930, -71.27621)
    VOLTAGE = 3.3
    BOARD_STATE_1 = True
    BOARD_STATE_2 = True
    BOARD_STATE_3 = False
    POWER_SUPPLY_STATE_1 = True
    POWER_SUPPLY_STATE_2 = False
    PAYLOAD_BOARD_STATE_1 = True
    TEMPERATURE = 100
    ORIENTATION = Orientation(1, 2, 3)
    OPEN_ROCKET_SIMULATION_FILENAME = "simulation.csv"
    A_ROCKET_PACKET_VERSION = 2019

    def setUp(self):
        self.data_widget = Mock(spec=DataWidget)
        self.data_producer = Mock(spec=DataProducer)
        self.consumer = MagicMock(spec=Consumer)
        self.consumer_factory = Mock(spec=ConsumerFactory)
        self.consumer_factory.create.return_value = self.consumer

        config = ConfigBuilder().build()

        self.controller = Controller(self.data_widget, self.data_producer, self.consumer_factory, config)
        self.controller.create_new_consumer(self.A_ROCKET_PACKET_VERSION)

    def test_update_should_update_consumer(self):
        self.controller.update()

        self.consumer.update.assert_called_with()

    def test_update_should_update_plots_when_consumer_has_data(self):
        self.consumer.has_data.return_value = True
        self.setup_consumer_data()

        self.controller.update()

        self.data_widget.draw_altitude.assert_called_with(self.TIMESTAMPS, self.ALTITUDES)
        self.data_widget.draw_apogee.assert_called_with(self.APOGEE)
        self.data_widget.draw_map.assert_called_with(self.EASTINGS, self.NORTHINGS)
        self.data_widget.show_current_coordinates.assert_called_with(self.GPS_COORDINATES)
        self.data_widget.draw_voltage.assert_called_with(self.VOLTAGE)

    def test_update_should_update_leds_when_consumer_has_data(self):
        self.consumer.has_data.return_value = True
        self.setup_consumer_data()

        self.controller.update()

        self.assert_leds_updated()

    def test_update_should_update_thermometer_when_consumer_has_data(self):
        self.consumer.has_data.return_value = True
        self.consumer.get_average_temperature.return_value = self.TEMPERATURE

        self.controller.update()

        self.data_widget.set_thermometer_value.assert_called_with(self.TEMPERATURE)

    def test_update_should_update_3d_model_when_consumer_has_data(self):
        self.consumer.has_data.return_value = True
        self.consumer.get_rocket_orientation.return_value = self.ORIENTATION

        self.controller.update()

        self.data_widget.set_rocket_model_orientation.assert_called_with(self.ORIENTATION)

    def test_update_should_not_update_ui_when_consumer_has_no_data(self):
        self.consumer.has_data.return_value = False

        self.controller.update()

        self.assert_ui_not_updated()

    def test_update_should_clear_consumer(self):
        self.controller.update()

        self.consumer.clear.assert_called_with()

    @patch("src.controller.OpenRocketSimulation")
    def test_add_open_rocket_simulation_should_show_simulation_in_ui(self, simulation):
        simulation_mock = simulation.return_value

        self.controller.add_open_rocket_simulation(self.OPEN_ROCKET_SIMULATION_FILENAME)

        self.data_widget.show_simulation.assert_called_with(simulation_mock)

    @patch("src.controller.OpenRocketSimulation")
    def test_add_open_rocket_simulation_should_notify_message_listeners_when_simulation_loaded(self, _):
        message_listener = Mock(spec=MessageListener)
        self.controller.register_message_listener(message_listener)

        self.controller.add_open_rocket_simulation(self.OPEN_ROCKET_SIMULATION_FILENAME)

        message_listener.notify.assert_called_with(AnyStringWith(self.OPEN_ROCKET_SIMULATION_FILENAME),
                                                   MessageType.INFO)

    @patch("src.controller.OpenRocketSimulation")
    def test_add_open_rocket_simulation_should_notify_message_listeners_when_simulation_loading_fails(self, simulation):
        error_message = "error message"
        simulation.side_effect = InvalidOpenRocketSimulationFileException(error_message)
        message_listener = Mock(spec=MessageListener)
        self.controller.register_message_listener(message_listener)

        self.controller.add_open_rocket_simulation(self.OPEN_ROCKET_SIMULATION_FILENAME)

        message_listener.notify.assert_called_with(AnyStringWith(error_message), MessageType.ERROR)

    def test_create_new_consumer_should_delegate_to_factory(self):
        self.controller.consumer = None

        self.controller.create_new_consumer(self.A_ROCKET_PACKET_VERSION)

        self.assertEqual(self.controller.consumer, self.consumer)

    def setup_consumer_data(self):
        data = {"altitude_feet": self.ALTITUDES, "apogee": self.APOGEE, "voltage": self.VOLTAGE,
                "acquisition_board_state_1": [self.BOARD_STATE_1], "acquisition_board_state_2": [self.BOARD_STATE_2],
                "acquisition_board_state_3": [self.BOARD_STATE_3], "power_supply_state_1": [self.POWER_SUPPLY_STATE_1],
                "power_supply_state_2": [self.POWER_SUPPLY_STATE_2],
                "payload_board_state_1": [self.PAYLOAD_BOARD_STATE_1], "time_stamp": self.TIMESTAMPS}
        self.consumer.__getitem__.side_effect = lambda arg: data[arg]
        self.consumer.get_projected_coordinates.return_value = (self.EASTINGS, self.NORTHINGS)
        self.consumer.get_last_gps_coordinates.return_value = self.GPS_COORDINATES

    def assert_leds_updated(self):
        calls = [call(1, self.BOARD_STATE_1), call(2, self.BOARD_STATE_2), call(3, self.BOARD_STATE_3),
                 call(4, self.POWER_SUPPLY_STATE_1), call(5, self.POWER_SUPPLY_STATE_2),
                 call(6, self.PAYLOAD_BOARD_STATE_1)]
        self.data_widget.set_led_state.assert_has_calls(calls, any_order=True)

    def assert_ui_not_updated(self):
        self.data_widget.draw_altitude.assert_not_called()
        self.data_widget.draw_apogee.assert_not_called()
        self.data_widget.draw_map.assert_not_called()
        self.data_widget.draw_voltage.assert_not_called()
        self.data_widget.set_led_state.assert_not_called()
        self.data_widget.set_thermometer_value.assert_not_called()
        self.data_widget.set_rocket_model_orientation.assert_not_called()
