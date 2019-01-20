from src.config import RocketPacketConfig, SerialPortConfig, Config


class ConfigBuilder:

    def __init__(self):
        self.rocket_packet_version = 2018
        self.sampling_frequency = 1.0

        self.start_character = b's'
        self.baudrate = 9600
        self.timeout = 1

        self.target_altitude = 10000
        self.gps_device_name = "gps"
        self.gui_fps = 30

    def build(self):
        rocket_packet_config = RocketPacketConfig(self.rocket_packet_version, self.sampling_frequency)
        serial_port_config = SerialPortConfig(self.start_character, self.baudrate, self.timeout)

        return Config(self.target_altitude, self.gps_device_name, self.gui_fps, rocket_packet_config,
                      serial_port_config)
