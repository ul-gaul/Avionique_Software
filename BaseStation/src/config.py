from configparser import ConfigParser


class RocketPacketConfig:
    def __init__(self, version: int, sampling_frequency: float):
        self.version = version
        self.sampling_frequency = sampling_frequency


class SerialPortConfig:
    def __init__(self, start_character: bytes, baudrate: int, timeout: int):
        self.start_character = start_character
        self.baudrate = baudrate
        self.timeout = timeout


class Config:
    def __init__(self, target_altitude: int, gps_device_name: str, gui_fps: float,
                 rocket_packet_config: RocketPacketConfig, serial_port_config: SerialPortConfig):
        self.target_altitude = target_altitude
        self.gps_device_name = gps_device_name
        self.gui_fps = gui_fps
        self.rocket_packet_config = rocket_packet_config
        self.serial_port_config = serial_port_config


class ConfigLoader:
    @staticmethod
    def load():
        config_parser = ConfigParser()
        config_parser.read("config.ini")

        rocket_packet_version = int(config_parser["rocket_packet"]["version"])
        sampling_frequency = float(config_parser["rocket_packet"]["sampling_frequency"])
        rocket_packet_config = RocketPacketConfig(rocket_packet_version, sampling_frequency)

        start_byte = bytes(config_parser["serial_port"]["start_character"], "utf-8")
        baudrate = int(config_parser["serial_port"]["baudrate"])
        timeout = int(config_parser["serial_port"]["timeout"])
        port_config = SerialPortConfig(start_byte, baudrate, timeout)

        target_altitude = int(config_parser["general"]["target_altitude"])
        gps_device_name = config_parser["gps"]["gps_device_name"]
        gui_fps = float(config_parser["general"]["gui_fps"])

        return Config(target_altitude, gps_device_name, gui_fps, rocket_packet_config, port_config)
