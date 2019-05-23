# -*- coding: utf-8 -*-
import os


class RocketPacket:

    def __init__(self, data_list=None):
        self.time_stamp = 0

        # Vitesse angulaire en radian par seconde
        self.angular_speed_x = 0
        self.angular_speed_y = 0
        self.angular_speed_z = 0

        # Acceleration en g
        self.acceleration_x = 0
        self.acceleration_y = 0
        self.acceleration_z = 0

        # Champs magnetiques en milli-gauss
        self.magnetometer_x = 0
        self.magnetometer_y = 0
        self.magnetometer_z = 0

        # Temps UTC
        self.utc_time = 0

        # Altitude en metres
        self.altitude = 0

        # Coordonnees GPS en degres
        self.latitude = 0
        self.longitude = 0
        self.ns_indicator = b''
        self.ew_indicator = b''

        # Temperature en degres Celsius
        self.temperature = 0

        # Orientation sous forme de quaternion
        self.quaternion_w = 0
        self.quaternion_x = 0
        self.quaternion_y = 0
        self.quaternion_z = 0

        # Etat des systemes
        self.acquisition_board_state_1 = 0
        self.acquisition_board_state_2 = 0
        self.acquisition_board_state_3 = 0
        self.power_supply_state_1 = 0
        self.power_supply_state_2 = 0
        self.payload_board_state_1 = 0

        # Donnees alimentation
        self.voltage = 0
        self.current = 0

        if data_list is not None:
            self._fill(data_list)

    def _fill(self, data_list):
        self.time_stamp = data_list[0]
        self.angular_speed_x = data_list[1]
        self.angular_speed_y = data_list[2]
        self.angular_speed_z = data_list[3]
        self.acceleration_x = data_list[4]
        self.acceleration_y = data_list[5]
        self.acceleration_z = data_list[6]
        self.altitude = data_list[7]
        self.latitude = data_list[8]
        self.longitude = data_list[9]
        self.temperature = data_list[10]
        self.quaternion_w = data_list[11]
        self.quaternion_x = data_list[12]
        self.quaternion_y = data_list[13]
        self.quaternion_z = data_list[14]
        self.acquisition_board_state_1 = data_list[15]
        self.acquisition_board_state_2 = data_list[16]
        self.acquisition_board_state_3 = data_list[17]
        self.power_supply_state_1 = data_list[18]
        self.power_supply_state_2 = data_list[19]
        self.payload_board_state_1 = data_list[20]
        self.voltage = data_list[21]
        self.current = data_list[22]
        self.magnetometer_x = data_list[23]
        self.magnetometer_y = data_list[24]
        self.magnetometer_z = data_list[25]
        self.pressure = data_list[26]
        self.ns_indicator = data_list[27]
        self.ew_indicator = data_list[28]
        self.utc_time = data_list[29]

    @staticmethod
    def keys():
        return ["time_stamp", "angular_speed_x", "angular_speed_y", "angular_speed_z", "acceleration_x",
                "acceleration_y", "acceleration_z", "altitude", "latitude", "longitude", "temperature", "quaternion_w",
                "quaternion_x", "quaternion_y", "quaternion_z", "acquisition_board_state_1",
                "acquisition_board_state_2", "acquisition_board_state_3", "power_supply_state_1",
                "power_supply_state_2", "payload_board_state_1", "voltage", "current", "magnetometer_x",
                "magnetometer_y", "magnetometer_z", "pressure", "ns_indicator", "ew_indicator", "utc_time"]

    def items(self):
        return self.__dict__.items()

    def __str__(self):
        string = ""
        for key in self.keys():
            string += str(self.__dict__[key]) + ","
        return string

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def print_data(self):
        # FIXME: convertir en methode __str__ et transferer la gestion de la console dans la fonction appelante
        os.system('cls' if os.name == 'nt' else 'clear')

        print("Time Stamp                : {}\n".format(self.time_stamp))

        print("Ang Speed X               : {}".format(self.angular_speed_x))
        print("Ang Speed Y               : {}".format(self.angular_speed_y))
        print("Ang Speed Z               : {}\n".format(self.angular_speed_z))

        print("Accel X                   : {}".format(self.acceleration_x))
        print("Accel Y                   : {}".format(self.acceleration_y))
        print("Accel Z                   : {}\n".format(self.acceleration_z))

        print("Altitude                  : {}\n".format(self.altitude))

        print("Latitude                  : {}".format(self.latitude))
        print("Longitude                 : {}".format(self.longitude))

        print("Temperature               : {}\n".format(self.temperature))

        print("Quaternion W              : {}".format(self.quaternion_w))
        print("Quaternion X              : {}".format(self.quaternion_x))
        print("Quaternion Y              : {}".format(self.quaternion_y))
        print("Quaternion Z              : {}\n".format(self.quaternion_z))

        print("Etat board acquisition 1  : {}".format(self.acquisition_board_state_1))
        print("Etat board acquisition 2  : {}".format(self.acquisition_board_state_2))
        print("Etat board acquisition 3  : {}".format(self.acquisition_board_state_3))
        print("Etat board alimentation 1 : {}".format(self.power_supply_state_1))
        print("Etat board alimentation 2 : {}".format(self.power_supply_state_2))
        print("Etat board payload        : {}\n".format(self.payload_board_state_1))

        print("Voltage                   : {}".format(self.voltage))
        print("Courant                   : {}\n".format(self.current))
