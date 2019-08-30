from typing import List
from typing import Tuple
import math

from src.data_processing.angular_position_calculator import AngularCalculator
from src.data_processing.apogee_calculator import ApogeeCalculator
from src.data_processing.gps.gps_coordinates import GpsCoordinates
from src.data_processing.gps.gps_processor import GpsProcessor
from src.data_processing.orientation_processor import OrientationProcessor
from src.data_processing.quaternion import Quaternion
from src.data_producer import DataProducer
from src.rocket_packet.rocket_packet import RocketPacket

METERS2FEET = 3.28084
ORIENTATION_INITIALISATION_DELAY_IN_SECONDS = 5


class Consumer: # TODO: add unit tests to this class
    def __init__(self, data_producer: DataProducer, apogee_calculator: ApogeeCalculator,
                 angular_calculator: AngularCalculator, gps_processor: GpsProcessor,
                 orientation_processor: OrientationProcessor):
        self.data_producer = data_producer
        self.apogee_calculator = apogee_calculator
        self.angular_calculator = angular_calculator
        self.gps_processor = gps_processor
        self.orientation_processor = orientation_processor
        self.rocket_packet_version = 2019
        self.data = {}
        self.create_keys_from_packet_format()
        self.data["altitude_feet"] = []
        self.data["apogee"] = []
        self.data["initial_roll"] = []
        self.data["initial_pitch"] = []
        self.data["initial_yaw"] = []
        self.first_integral_index = 0
        self.first_timestamp = 0
        self.initialising_orientation = True

    def create_keys_from_packet_format(self):
        for key in RocketPacket.keys():
            self.data[key] = []

    def update(self):
        rocket_packets = self.data_producer.get_available_rocket_packets()
        if len(rocket_packets) > 0:
            self.first_timestamp = rocket_packets[0].time_stamp
            for packet in rocket_packets:
                for key, value in packet.items():
                    self.data[key].append(value)
                self.data["altitude_feet"].append(packet.altitude * METERS2FEET)
                self.gps_processor.update(packet)
                self.orientation_processor.update(packet)

            self.manage_apogee(self.data["altitude_feet"])
            # self.angular_calculator.integrate_all(self.data["time_stamp"], self.data["angular_speed_x"],
            #                                       self.data["angular_speed_y"], self.data["angular_speed_z"])

    def __getitem__(self, key):
        return self.data[key]

    def manage_apogee(self, values: list):
        self.apogee_calculator.update(values)
        rep = self.apogee_calculator.get_apogee()
        if rep is not None:
            self.data["apogee"].append(rep[0])
            self.data["apogee"].append(rep[1])

    def get_rocket_rotation(self):
        return self.orientation_processor.get_rocket_rotation()
        # return Quaternion(self.angular_calculator.roll, self.angular_calculator.pitch, self.angular_calculator.yaw, 0)
        # return Quaternion.euler_radians_to_quaternion(self.angular_calculator.yaw, self.angular_calculator.pitch,
        #                                               self.angular_calculator.roll)

    def compute_rotation(self, packet: RocketPacket):   # TODO: remove this
        elapsed_time = self.data["time_stamp"][-1] - self.first_timestamp

        if self.initialising_orientation and elapsed_time >= ORIENTATION_INITIALISATION_DELAY_IN_SECONDS:
            roll = self.average(self.data["initial_roll"])
            pitch = self.average(self.data["initial_roll"])
            yaw = self.average(self.data["initial_yaw"])
            self.angular_calculator.set_initial_angular_position(roll, pitch, yaw)
            self.first_integral_index = len(self.data["time_stamp"]) - 1
            self.initialising_orientation = False

        if elapsed_time < ORIENTATION_INITIALISATION_DELAY_IN_SECONDS:
            spherical_coordinates = self.to_spherical(packet.acceleration_x, packet.acceleration_y,
                                                      packet.acceleration_z)
            self.data["initial_roll"].append(math.sin(spherical_coordinates[1]) * spherical_coordinates[2])
            self.data["initial_pitch"].append(math.cos(spherical_coordinates[1]) * spherical_coordinates[2])
            self.data["initial_yaw"].append(0)
            self.initialising_orientation = True
        else:
            self.angular_calculator.integrate_all(self.data["time_stamp"][self.first_integral_index:],
                                                  self.data["angular_speed_x"][self.first_integral_index:],
                                                  self.data["angular_speed_y"][self.first_integral_index:],
                                                  self.data["angular_speed_z"][self.first_integral_index:])
            self.initialising_orientation = False

    def get_rocket_last_quaternion(self):
        return (self.data["quaternion_w"][-1], self.data["quaternion_x"][-1], self.data["quaternion_y"][-1],
                self.data["quaternion_z"][-1])

    def get_rocket_last_angular_velocity(self):
        return self.data["angular_speed_x"][-1], self.data["angular_speed_y"][-1], self.data["angular_speed_z"][-1]

    def get_average_temperature(self):
        return self.data["temperature"][-1]

    def get_projected_coordinates(self) -> Tuple[List, List]:
        return self.gps_processor.get_projected_coordinates()

    def get_last_gps_coordinates(self) -> GpsCoordinates:
        return self.gps_processor.get_last_coordinates()

    def clear(self):
        for data_list in self.data.values():
            data_list.clear()

        self.gps_processor.reset()
        self.orientation_processor.reset()

    def has_data(self):
        return len(self.data["time_stamp"]) != 0
