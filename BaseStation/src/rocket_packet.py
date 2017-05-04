# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 12:03:00 2016

@author: Maxime
"""
import os


class RocketPacket:
    def __init__(self, data_list):
        self.time_stamp = data_list[0]

        # Vitesse angulaire en radian par seconde
        self.angular_speed_x = data_list[1]
        self.angular_speed_y = data_list[2]
        self.angular_speed_z = data_list[3]

        # Acceleration en g
        self.acceleration_x = data_list[4]
        self.acceleration_y = data_list[5]
        self.acceleration_z = data_list[6]

        # Champ magnetique en Gauss
        self.magnetic_field_x = data_list[7]
        self.magnetic_field_y = data_list[8]
        self.magnetic_field_z = data_list[9]

        # Altitude en metres
        self.altitude = data_list[10]

        # Coordonnees GPS en degres
        self.latitude_1 = data_list[11]
        self.longitude_1 = data_list[12]
        self.latitude_2 = data_list[13]
        self.longitude_2 = data_list[14]

        # Temperature en degres Celsius
        self.temperature_1 = data_list[15]
        self.temperature_2 = data_list[16]
        self.temperature_3 = data_list[17]
        # TODO: il peut y avoir plus de valeur de temperature

        self.date = data_list[18]

        # Orientation sous forme de quaternion
        self.quaternion_w = data_list[19]
        self.quaternion_x = data_list[20]
        self.quaternion_y = data_list[21]
        self.quaternion_z = data_list[22]

        # etat des systemes
        self.acquisition_board_state_1 = data_list[23]
        self.acquisition_board_state_2 = data_list[24]
        self.acquisition_board_state_3 = data_list[25]
        self.power_supply_state_1 = data_list[26]
        self.power_supply_state_2 = data_list[27]
        self.payload_board_state_1 = data_list[28]

        # donnees alimentation
        self.voltage = data_list[29]
        self.current = data_list[30]

        # donnees payload
        self.angSpeed_payload_x = data_list[31]
        self.angSpeed_payload_y = data_list[32]
        self.angSpeed_payload_z = data_list[33]

        # donnees de controler
        self.camera = data_list[34]
        self.deployment = data_list[35]

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

        print("Magnet X                 : {}".format(self.magnetic_field_x))
        print("Magnet Y                 : {}".format(self.magnetic_field_y))
        print("Magnet Z                 : {}\n".format(self.magnetic_field_z))

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
