from src.data_processing.angular_position_calculator import AngularCalculator
from src.data_processing.apogee_calculator import ApogeeCalculator
from src.data_processing.gps.coordinate_conversion_strategy import CoordinateConversionStrategy
from src.data_processing.quaternion import Quaternion
from src.data_producer import DataProducer
from src.rocket_packet.rocket_packet import RocketPacket

METERS2FEET = 3.28084
CAMP_POSITION_MEASUREMENT_DELAY_IN_SECONDS = 10


class Consumer:
    def __init__(self, data_producer: DataProducer, apogee_calculator: ApogeeCalculator,
                 angular_calculator: AngularCalculator, coordinate_conversion_strategy: CoordinateConversionStrategy):
        self.data_producer = data_producer
        self.coordinate_conversion_strategy = coordinate_conversion_strategy
        self.apogee_calculator = apogee_calculator
        self.angular_calculator = angular_calculator
        self.rocket_packet_version = 2019
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
        self.last_latitude = 0.0
        self.last_longitude = 0.0
        self.first_timestamp = 0
        self.initializing_gps = True

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
                self.manage_coordinates(packet)

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

    def manage_coordinates(self, packet: RocketPacket):
        self.last_latitude, self.last_longitude = self.coordinate_conversion_strategy.to_decimal_degrees(
            packet.latitude, packet.longitude)
        easting, northing = self.coordinate_conversion_strategy.to_utm(packet.latitude, packet.longitude)

        elapsed_time = self.data["time_stamp"][-1] - self.first_timestamp

        if self.initializing_gps and elapsed_time >= CAMP_POSITION_MEASUREMENT_DELAY_IN_SECONDS:
            self.base_camp_easting = sum(self.data["initial_easting"]) / len(self.data["initial_easting"])
            self.base_camp_northing = sum(self.data["initial_northing"]) / len(self.data["initial_northing"])
            self.initializing_gps = False

        if elapsed_time < CAMP_POSITION_MEASUREMENT_DELAY_IN_SECONDS:
            self.data["initial_easting"].append(easting)
            self.data["initial_northing"].append(northing)
            self.data["easting"].append(0)
            self.data["northing"].append(0)
            self.initializing_gps = True
        else:
            self.data["easting"].append(easting - self.base_camp_easting)
            self.data["northing"].append(northing - self.base_camp_northing)
            self.initializing_gps = False

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

    def get_last_gps_coordinates(self):
        return self.last_latitude, self.last_longitude

    def clear(self):
        for data_list in self.data.values():
            data_list.clear()

        self.initializing_gps = True

    def has_data(self):
        return len(self.data["time_stamp"]) != 0

    def reset(self):
        self.clear()

        self.base_camp_easting = None
        self.base_camp_northing = None
        self.last_latitude = 0.0
        self.last_longitude = 0.0

        self.first_timestamp = 0

        self.apogee_calculator.reset()
        self.angular_calculator.reset()
