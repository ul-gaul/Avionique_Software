from typing import List
from typing import Tuple

from src.data_processing.angular_position_calculator import AngularCalculator
from src.data_processing.apogee_calculator import ApogeeCalculator
from src.data_processing.gps.gps_processor import GpsProcessor
from src.data_processing.quaternion import Quaternion
from src.data_producer import DataProducer
from src.rocket_packet.rocket_packet import RocketPacket

METERS2FEET = 3.28084


class Consumer:
    def __init__(self, data_producer: DataProducer, apogee_calculator: ApogeeCalculator,
                 angular_calculator: AngularCalculator, gps_processor: GpsProcessor):
        self.data_producer = data_producer
        self.apogee_calculator = apogee_calculator
        self.angular_calculator = angular_calculator
        self.gps_processor = gps_processor
        self.rocket_packet_version = 2019
        self.data = {}
        self.create_keys_from_packet_format()
        self.data["altitude_feet"] = []
        self.data["apogee"] = []

    def create_keys_from_packet_format(self):
        for key in RocketPacket.keys():
            self.data[key] = []

    def update(self):
        rocket_packets = self.data_producer.get_available_rocket_packets()
        if len(rocket_packets) > 0:
            for packet in rocket_packets:
                for key, value in packet.items():
                    self.data[key].append(value)
                self.data["altitude_feet"].append(packet.altitude * METERS2FEET)
                self.gps_processor.update(packet)

            self.manage_apogee(self.data["altitude_feet"])
            self.angular_calculator.integrate_all(self.data["time_stamp"], self.data["angular_speed_x"],
                                                  self.data["angular_speed_y"], self.data["angular_speed_z"])

    def __getitem__(self, key):
        return self.data[key]

    def manage_apogee(self, values: list):
        self.apogee_calculator.update(values)
        rep = self.apogee_calculator.get_apogee()
        if rep is not None:
            self.data["apogee"].append(rep[0])
            self.data["apogee"].append(rep[1])

    def get_rocket_rotation(self):
        return Quaternion.euler_radians_to_quaternion(self.angular_calculator.yaw, self.angular_calculator.pitch,
                                                      self.angular_calculator.roll)

    def get_rocket_last_quaternion(self):
        return (self.data["quaternion_w"][-1], self.data["quaternion_x"][-1], self.data["quaternion_y"][-1],
                self.data["quaternion_z"][-1])

    def get_rocket_last_angular_velocity(self):
        return self.data["angular_speed_x"][-1], self.data["angular_speed_y"][-1], self.data["angular_speed_z"][-1]

    def get_average_temperature(self):
        return self.data["temperature"][-1]

    def get_projected_coordinates(self) -> Tuple[List, List]:
        return self.gps_processor.get_projected_coordinates()

    def get_last_gps_coordinates(self) -> Tuple[float, float]:
        return self.gps_processor.get_last_coordinates()

    def clear(self):
        for data_list in self.data.values():
            data_list.clear()

        self.gps_processor.reset()

    def has_data(self):
        return len(self.data["time_stamp"]) != 0
