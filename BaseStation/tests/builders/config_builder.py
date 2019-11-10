from src.config import RocketPacketConfig, SerialPortConfig, Config, GpsConfig, OrientationConfig
from src.data_processing.gps.utm_zone import UTMZone


class ConfigBuilder:
    def __init__(self):
        self.rocket_packet_version = 2018
        self.sampling_frequency = 1.0

        self.gps_device_name = "gps"
        self.utm_zone = UTMZone.zone_13S
        self.gps_initialisation_delay = 10

        self.orientation_initialization_delay = 0

        self.start_character = b's'
        self.baudrate = 9600
        self.timeout = 1

        self.target_altitude = 10000
        self.gui_fps = 30.0

    def with_rocket_packet_version(self, version: int):
        self.rocket_packet_version = version
        return self

    def with_gui_fps(self, frame_per_second: float):
        self.gui_fps = frame_per_second
        return self

    def build(self):
        rocket_packet_config = RocketPacketConfig(self.rocket_packet_version, self.sampling_frequency)
        gps_config = GpsConfig(self.gps_device_name, self.utm_zone, self.gps_initialisation_delay)
        orientation_config = OrientationConfig(self.orientation_initialization_delay)
        serial_port_config = SerialPortConfig(self.start_character, self.baudrate, self.timeout)

        return Config(self.target_altitude, self.gui_fps, rocket_packet_config, gps_config, orientation_config,
                      serial_port_config)
