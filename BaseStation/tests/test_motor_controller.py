import unittest
from unittest.mock import Mock, MagicMock

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QCloseEvent

from src.data_processing.consumer_factory import ConsumerFactory
from src.motor_controller import MotorController
from src.realtime.serial_data_producer import SerialDataProducer
from src.save import SaveManager
from src.ui.motor_widget import MotorWidget
from tests.builders.config_builder import ConfigBuilder


class MotorControllerTest(unittest.TestCase):

    def setUp(self):
        self.motor_widget = Mock(spec=MotorWidget)
        self.serial_data_producer = Mock(spec=SerialDataProducer)
        self.consumer_factory = MagicMock(spec=ConsumerFactory)
        self.save_manager = Mock(spec=SaveManager)
        self.event = Mock(spec=QCloseEvent)

        self.config = ConfigBuilder().with_rocket_packet_version(self.A_ROCKET_PACKET_VERSION).build()
        self.qtimer = Mock(spec=QTimer)

        self.motor_controller = MotorController(self.motor_widget, self.serial_data_producer,
                                                       self.consumer_factory, self.save_manager, self.config,
                                                       self.qtimer)
        self.motor_controller.is_running = False
