from pyproj import Proj
from BaseStation.src.rocket_packet import RocketPacket
from BaseStation.src.producer import Producer


METERS2FEET = 3.28084
CAMP_POSITION_MEASUREMENT_DELAY = 10  # in seconds


class Consumer:

    def __init__(self, producer, sampling_frequency):
        assert isinstance(producer, Producer)
        self.producer = producer
        self.sampling_frequency = sampling_frequency
        self.data = {}
        self.has_new_data = False
        self.create_keys_from_packet_format()
        self.data["altitude_feet"] = []
        self.data["easting"] = []
        self.data["northing"] = []
        self.data["initial_easting"] = []
        self.data["initial_northing"] = []
        self.base_camp_easting = None
        self.base_camp_northing = None
        self.geo_converter = Proj("+proj=utm +zone=13s, +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
        #self.led_callback = None

    def create_keys_from_packet_format(self):
        for key in RocketPacket.keys():
            self.data[key] = []

    def update(self):
        rocket_packets = self.producer.get_data()
        if len(rocket_packets) > 0:
            for packet in rocket_packets:
                #print(packet)
                for key, value in packet.items():
                    self.data[key].append(value)
                self.data["altitude_feet"].append(packet.altitude * METERS2FEET)
                self.manage_coordinates(packet)
                #self.update_leds()
            self.has_new_data = True

    def __getitem__(self, key):
        return self.data[key]

    def manage_coordinates(self, packet):
        easting, northing = self.geo_converter(packet.longitude_1, packet.latitude_1)

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
        return self.data["quaternion_w"][-1], self.data["quaternion_x"][-1], self.data["quaternion_y"][-1], \
               self.data["quaternion_z"][-1]

    def get_average_temperature(self):
        return self.data["temperature_1"][-1]

    # def update_leds(self):
    #     if self.led_callback is not None:
    #         #self.data["acquisition_board_state_1"][-1]
    #         pass
    #
    # def _update_led(self, led_name, led_num):
    #     if len(self.data[led_name])

