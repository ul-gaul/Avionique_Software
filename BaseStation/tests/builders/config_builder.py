from src.config import RocketPacketConfig, SerialPortConfig, Config, GpsConfig
from src.data_processing.gps.utm_zone import UTMZone


class ConfigBuilder:
    def __init__(self):
        self.rocket_packet_version = 2018
        self.sampling_frequency = 1.0

        self.gps_device_name = "gps"
        self.utm_zone = UTMZone.zone_13S
        self.origin_measurement_delay = 10

        self.start_character = b's'
        self.baudrate = 9600
        self.timeout = 1

        self.target_altitude = 10000
        self.gui_fps = 30

    def with_rocket_packet_version(self, version: int):
        self.rocket_packet_version = version
        return self

    def build(self):
        rocket_packet_config = RocketPacketConfig(self.rocket_packet_version, self.sampling_frequency)
        gps_config = GpsConfig(self.gps_device_name, self.utm_zone, self.origin_measurement_delay)
        serial_port_config = SerialPortConfig(self.start_character, self.baudrate, self.timeout)

        return Config(self.target_altitude, self.gui_fps, rocket_packet_config, gps_config, serial_port_config)
