# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 12:03:00 2016

@author: Maxime
"""
import os


class RocketPacket:
    format = "<ffffffffffffffffffffBBBBBBfffffBB"
    size_in_bytes = 108

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

        # Altitude en metres
        self.altitude = 0

        # Coordonnees GPS en degres
        self.latitude_1 = 0
        self.longitude_1 = 0
        self.latitude_2 = 0
        self.longitude_2 = 0

        # Temperature en degres Celsius
        self.temperature_1 = 0
        self.temperature_2 = 0
        self.temperature_3 = 0  # average between temperature_1 and temperature_2

        self.date = 0

        # Orientation sous forme de quaternion
        self.quaternion_w = 0
        self.quaternion_x = 0
        self.quaternion_y = 0
        self.quaternion_z = 0

        # etat des systemes
        self.acquisition_board_state_1 = 0
        self.acquisition_board_state_2 = 0
        self.acquisition_board_state_3 = 0
        self.power_supply_state_1 = 0
        self.power_supply_state_2 = 0
        self.payload_board_state_1 = 0

        # donnees alimentation
        self.voltage = 0
        self.current = 0

        # donnees payload
        self.angSpeed_payload_x = 0
        self.angSpeed_payload_y = 0
        self.angSpeed_payload_z = 0

        # donnees de controler
        self.camera = 0
        self.deployment = 0

        if data_list is not None:
            self.fill(data_list)

    def fill(self, data_list):
        self.time_stamp = data_list[0]
        self.angular_speed_x = data_list[1]
        self.angular_speed_y = data_list[2]
        self.angular_speed_z = data_list[3]
        self.acceleration_x = data_list[4]
        self.acceleration_y = data_list[5]
        self.acceleration_z = data_list[6]
        self.altitude = data_list[7]
        self.latitude_1 = data_list[8]
        self.longitude_1 = data_list[9]
        self.latitude_2 = data_list[10]
        self.longitude_2 = data_list[11]
        self.temperature_1 = data_list[12]
        self.temperature_2 = data_list[13]
        self.temperature_3 = data_list[14]
        self.date = data_list[15]
        self.quaternion_w = data_list[16]
        self.quaternion_x = data_list[17]
        self.quaternion_y = data_list[18]
        self.quaternion_z = data_list[19]
        self.acquisition_board_state_1 = data_list[20]
        self.acquisition_board_state_2 = data_list[21]
        self.acquisition_board_state_3 = data_list[22]
        self.power_supply_state_1 = data_list[23]
        self.power_supply_state_2 = data_list[24]
        self.payload_board_state_1 = data_list[25]
        self.voltage = data_list[26]
        self.current = data_list[27]
        self.angSpeed_payload_x = data_list[28]
        self.angSpeed_payload_y = data_list[29]
        self.angSpeed_payload_z = data_list[30]
        self.camera = data_list[31]
        self.deployment = data_list[32]

    @staticmethod
    def keys():
        return ["time_stamp", "angular_speed_x", "angular_speed_y", "angular_speed_z", "acceleration_x",
                "acceleration_y", "acceleration_z", "altitude", "latitude_1", "longitude_1", "latitude_2",
                "longitude_2", "temperature_1", "temperature_2", "temperature_3", "date", "quaternion_w",
                "quaternion_x", "quaternion_y", "quaternion_z", "acquisition_board_state_1",
                "acquisition_board_state_2", "acquisition_board_state_3", "power_supply_state_1",
                "power_supply_state_2", "payload_board_state_1", "voltage", "current", "angSpeed_payload_x",
                "angSpeed_payload_y", "angSpeed_payload_z", "camera", "deployment"]

    def items(self):
        return self.__dict__.items()

    def __str__(self):
        string = ""
        for key in self.keys():
            string += str(self.__dict__[key]) + ","
        return string

    def print_data(self):
        # FIXME: convertir en methode __str__ et transferer la gestion de la console dans la fonction appelante
        os.system('cls' if os.name == 'nt' else 'clear')

        print("Time Stamp               : {}\n".format(self.time_stamp))

        print("Ang Speed X              : {}".format(self.angular_speed_x))
        print("Ang Speed Y              : {}".format(self.angular_speed_y))
        print("Ang Speed Z              : {}\n".format(self.angular_speed_z))

        print("Accel X                  : {}".format(self.acceleration_x))
        print("Accel Y                  : {}".format(self.acceleration_y))
        print("Accel Z                  : {}\n".format(self.acceleration_z))

        print("Altitude                 : {}\n".format(self.altitude))

        print("Latitude 1               : {}".format(self.latitude_1))
        print("Longitude 1              : {}".format(self.longitude_1))
        print("Latitude 2               : {}".format(self.latitude_2))
        print("Longitude 2              : {}\n".format(self.longitude_2))

        print("Temp 1                   : {}".format(self.temperature_1))
        print("Temp 2                   : {}".format(self.temperature_2))
        print("Temp 3                   : {}\n".format(self.temperature_3))

        print("Date                      : {}\n".format(self.date))

        print("Quaternion W                   : {}".format(self.quaternion_w))
        print("Quaternion X                   : {}".format(self.quaternion_x))
        print("Quaternion Y                   : {}".format(self.quaternion_y))
        print("Quaternion Z                   : {}\n".format(self.quaternion_z))

        print("Etat board acquisition 1  : {}".format(self.acquisition_board_state_1))
        print("Etat board acquisition 2  : {}".format(self.acquisition_board_state_2))
        print("Etat board acquisition 3  : {}".format(self.acquisition_board_state_3))
        print("Etat board alimentation 1 : {}".format(self.power_supply_state_1))
        print("Etat board alimentation 2 : {}".format(self.power_supply_state_2))
        print("Etat board payload        : {}\n".format(self.payload_board_state_1))

        print("Voltage                   : {}".format(self.voltage))
        print("Courant                   : {}\n".format(self.current))

        print("Payload Ang Speed X       : {}".format(self.angSpeed_payload_x))
        print("Payload Ang Speed Y       : {}".format(self.angSpeed_payload_y))
        print("Payload Ang Speed Z       : {}\n".format(self.angSpeed_payload_z))

        print("Camera                    : {}".format(self.camera))
        print("Deploiment                : {}\n".format(self.deployment))
