from src.data_processing.angular_position_calculator import AngularCalculator
from src.data_processing.apogee_calculator import ApogeeCalculator
from src.data_processing.utm_zone import UTMZone

from src.data_processing.geo_coordinate_converter import GeoCoordinateConverter
from src.data_producer import DataProducer
from src.rocket_packet import RocketPacket

from src.data_processing.quaternion import Quaternion

METERS2FEET = 3.28084
CAMP_POSITION_MEASUREMENT_DELAY = 10  # in seconds


class Consumer:

    def __init__(self, data_producer: DataProducer, sampling_frequency: float, apogee_calculator: ApogeeCalculator, angular_calculator: AngularCalculator):
        self.data_producer = data_producer
        self.sampling_frequency = sampling_frequency
        self.data = {}
        self.create_keys_from_packet_format()
        self.data["altitude_feet"] = []
        self.data["easting"] = []
        self.data["northing"] = []
        self.data["initial_easting"] = []
        self.data["initial_northing"] = []
        self.data["apogee"] = []
        self.base_camp_easting = None
        self.base_camp_northing = None
        self.coordinate_converter = GeoCoordinateConverter(UTMZone.zone_13S)
        self.apogee_calculator = apogee_calculator
        self.angular_calculator = angular_calculator

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
                self.manage_coordinates(packet)

            self.manage_apogee(self.data["altitude_feet"])
            self.angular_calculator.integrate_all(self.data["angular_speed_x"], self.data["angular_speed_y"], self.data["angular_speed_z"])

    def __getitem__(self, key):
        return self.data[key]

    def manage_apogee(self, values: list):
        self.apogee_calculator.update(values)
        rep = self.apogee_calculator.get_apogee()
        if rep is not None:
            self.data["apogee"].append(rep[0])
            self.data["apogee"].append(rep[1])

    def manage_coordinates(self, packet):
        easting, northing = self.coordinate_converter.from_long_lat_to_utm(packet.longitude, packet.latitude)

        num_packets_received = len(self.data["time_stamp"])

        if num_packets_received == CAMP_POSITION_MEASUREMENT_DELAY * self.sampling_frequency:
            self.base_camp_easting = sum(self.data["initial_easting"]) / len(self.data["initial_easting"])
            self.base_camp_northing = sum(self.data["initial_northing"]) / len(self.data["initial_northing"])

        if num_packets_received < CAMP_POSITION_MEASUREMENT_DELAY * self.sampling_frequency:
            self.data["initial_easting"].append(easting)
            self.data["initial_northing"].append(northing)
            self.data["easting"].append(0)
            self.data["northing"].append(0)
        else:
            self.data["easting"].append(easting - self.base_camp_easting)
            self.data["northing"].append(northing - self.base_camp_northing)

    def get_rocket_rotation(self):
        return Quaternion.euler_radians_to_quaternion(self.angular_calculator.yaw, self.angular_calculator.pitch, self.angular_calculator.roll)

    def get_rocket_last_quaternion(self):
        return self.data["quaternion_w"][-1], self.data["quaternion_x"][-1], self.data["quaternion_y"][-1], self.data["quaternion_z"][-1]

    def get_rocket_last_angular_velocity(self):
        return self.data["angular_speed_x"][-1], self.data["angular_speed_y"][-1], self.data["angular_speed_z"][-1]

    def get_average_temperature(self):
        return self.data["temperature"][-1]

    def clear(self):
        for data_list in self.data.values():
            data_list.clear()

    def has_data(self):
        return len(self.data["time_stamp"]) != 0

    def reset(self):
        self.clear()

        self.base_camp_easting = None
        self.base_camp_northing = None

        self.apogee_calculator.reset()
        self.angular_calculator.reset()