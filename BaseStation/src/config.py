from configparser import ConfigParser

from src.data_processing.gps.utm_zone import UTMZone


class RocketPacketConfig:
    def __init__(self, version: int, sampling_frequency: float):
        self.version = version
        self.sampling_frequency = sampling_frequency


class SerialPortConfig:
    def __init__(self, start_character: bytes, baudrate: int, timeout: int):
        self.start_character = start_character
        self.baudrate = baudrate
        self.timeout = timeout


class GpsConfig:
    def __init__(self, gps_device_name: str, utm_zone: UTMZone, initialization_delay: int):
        self.gps_device_name = gps_device_name
        self.utm_zone = utm_zone
        self.initialization_delay = initialization_delay


class OrientationConfig:
    def __init__(self, initialization_delay_in_seconds: float):
        self.initialization_delay_in_seconds = initialization_delay_in_seconds


class Config:
    def __init__(self, target_altitude: int, gui_fps: float, rocket_packet_config: RocketPacketConfig,
                 gps_config: GpsConfig, orientation_config: OrientationConfig, serial_port_config: SerialPortConfig):
        self.target_altitude = target_altitude
        self.gui_fps = gui_fps
        self.rocket_packet_config = rocket_packet_config
        self.gps_config = gps_config
        self.orientation_config = orientation_config
        self.serial_port_config = serial_port_config


class ConfigLoader:
    @staticmethod
    def load():
        config_parser = ConfigParser()
        config_parser.read("config.ini")

        rocket_packet_version = int(config_parser["rocket_packet"]["version"])
        sampling_frequency = float(config_parser["rocket_packet"]["sampling_frequency"])
        rocket_packet_config = RocketPacketConfig(rocket_packet_version, sampling_frequency)

        gps_device_name = config_parser["gps"]["gps_device_name"]
        utm_zone = UTMZone(config_parser["gps"]["utm_zone"])
        gps_initialization_delay = int(config_parser["gps"]["initialization_delay_in_seconds"])
        gps_config = GpsConfig(gps_device_name, utm_zone, gps_initialization_delay)

        orientation_initialization_delay = float(config_parser["orientation"]["initialization_delay_in_seconds"])
        orientation_config = OrientationConfig(orientation_initialization_delay)

        start_byte = bytes(config_parser["serial_port"]["start_character"], "utf-8")
        baudrate = int(config_parser["serial_port"]["baudrate"])
        timeout = int(config_parser["serial_port"]["timeout"])
        port_config = SerialPortConfig(start_byte, baudrate, timeout)

        target_altitude = int(config_parser["general"]["target_altitude"])
        gui_fps = float(config_parser["general"]["gui_fps"])

        return Config(target_altitude, gui_fps, rocket_packet_config, gps_config, orientation_config, port_config)
