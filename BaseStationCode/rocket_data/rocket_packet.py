# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 12:03:00 2016

@author: Maxime
"""
import struct
import os


class RocketPacket:
    def __init__(self, data_buffer):
        self.format = "<ffffffffffffffffffffffBBBBBBfffffBBB"
        self.data_buffer = data_buffer
        new_data = struct.unpack(self.format, data_buffer)

        self.time_stamp = new_data[0]

        # Vitesse angulaire en radian par seconde
        self.angular_speed_x = new_data[1]
        self.angular_speed_y = new_data[2]
        self.angular_speed_z = new_data[3]

        # Acceleration en g
        self.acceleration_x = new_data[4]
        self.acceleration_y = new_data[5]
        self.acceleration_z = new_data[6]

        # Champ magnetique en Gauss
        self.magnetic_field_x = new_data[7]
        self.magnetic_field_y = new_data[8]
        self.magnetic_field_z = new_data[9]

        # Altitude en metres
        self.altitude = new_data[10]

        # Coordonnees GPS en degres
        self.latitude_1 = new_data[11]
        self.longitude_1 = new_data[12]
        self.latitude_2 = new_data[13]
        self.longitude_2 = new_data[14]

        # Temperature en degres Celsius
        self.temperature_1 = new_data[15]
        self.temperature_2 = new_data[16]
        self.temperature_3 = new_data[17]
        # TODO: il peut y avoir plus de valeur de temperature

        self.date = new_data[18]

        # Orientation en degres TODO: remplacer par un quaternion
        self.euler_x = new_data[19]
        self.euler_y = new_data[20]
        self.euler_z = new_data[21]

        # etat des systemes
        self.acquisition_board_state_1 = new_data[22]
        self.acquisition_board_state_2 = new_data[23]
        self.acquisition_board_state_3 = new_data[24]
        self.power_supply_state_1 = new_data[25]
        self.power_supply_state_2 = new_data[26]
        self.payload_board_state_1 = new_data[27]

        # donnees alimentation
        self.voltage = new_data[28]
        self.current = new_data[29]

        # donnees payload
        self.angSpeed_payload_x = new_data[30]
        self.angSpeed_payload_y = new_data[31]
        self.angSpeed_payload_z = new_data[32]

        # donnees de controler
        self.camera = new_data[33]
        self.deployment = new_data[34]

        self.checksum = new_data[35]

    def validate_checksum(self):
        # TODO: s'entendre avec l'equipe d'acquisition pour la formule a utiliser
        checksum = sum(self.data_buffer[0:-2]) % 256
        if checksum == self.checksum:
            return True
        else:
            print("Invalid Checksum : data = {}, calculated = {}".format(self.checksum, checksum))
            return False

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

        print("Euler X                   : {}".format(self.euler_x))
        print("Euler Y                   : {}".format(self.euler_y))
        print("Euler Z                   : {}\n".format(self.euler_z))

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

        print("Checksum                  : {}".format(self.checksum))
