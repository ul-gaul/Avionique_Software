from configparser import ConfigParser


class SerialPortConfig:
    def __init__(self, start_character: bytes, baudrate: int, timeout: int):
        self.start_character = start_character
        self.baudrate = baudrate
        self.timeout = timeout


class Config:
    def __init__(self, target_altitude: int, gps_device_name: str, rocket_packet_version: int, gui_fps: float,
                 serial_port_config: SerialPortConfig):
        self.target_altitude = target_altitude
        self.gps_device_name = gps_device_name
        self.rocket_packet_version = rocket_packet_version
        self.gui_fps = gui_fps
        self.serial_port_config = serial_port_config


class ConfigLoader:
    @staticmethod
    def load():
        config_parser = ConfigParser()
        config_parser.read("config.ini")

        start_byte = bytes(config_parser["serial_port"]["start_character"], "utf-8")
        baudrate = int(config_parser["serial_port"]["baudrate"])
        timeout = int(config_parser["serial_port"]["timeout"])
        port_config = SerialPortConfig(start_byte, baudrate, timeout)

        target_altitude = int(config_parser["general"]["target_altitude"])
        gps_device_name = config_parser["gps"]["gps_device_name"]
        rocket_packet_version = int(config_parser["general"]["rocket_packet_version"])
        gui_fps = float(config_parser["general"]["gui_fps"])

        return Config(target_altitude, gps_device_name, rocket_packet_version, gui_fps, port_config)
