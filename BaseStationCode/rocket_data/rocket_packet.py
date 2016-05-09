# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 12:03:00 2016

@author: Maxime
"""

import struct


class RocketData:

    DATA_FORMAT = ">fffffffffffffff"

    # def __init__(self, p_timeStamp, p_angSpeedX, p_angSpeedY, p_angSpeedZ, \
    #              p_accelX, p_accelY, p_accelZ, p_magnetX, p_magnetY, p_magnetZ, \
    #              p_altitude, p_latitude, p_longitude, p_temperature, p_stress1):
    #
    #     """Initialization of the data with the parameters"""
    #     self.timeStamp = p_timeStamp
    #
    #     self.angSpeedX = p_angSpeedX
    #     self.angSpeedY = p_angSpeedY
    #     self.angSpeedZ = p_angSpeedZ
    #
    #     self.accelX = p_accelX
    #     self.accelY = p_accelY
    #     self.accelZ = p_accelZ
    #
    #     self.magnetX = p_magnetX
    #     self.magnetY = p_magnetY
    #     self.magnetZ = p_magnetZ
    #
    #     self.altitude = p_altitude
    #
    #     self.latitude = p_latitude
    #     self.longitude = p_longitude
    #
    #     self.temperature = p_temperature
    #
    #     self.stress1 = p_stress1
    #
    #     """Creation of the structure containing the data"""
    #     self.data = [self.timeStamp, \
    #                 self.angSpeedX, self.angSpeedY, self.angSpeedZ, \
    #                 self.accelX, self.accelY, self.accelZ, \
    #                 self.magnetX, self.magnetY, self.magnetZ, \
    #                 self.altitude, self.latitude, self.longitude, \
    #                 self.temperature, self.stress1]

    def __init__(self):
        self.timeStamp = 0

        self.angular_speed_x = 0
        self.angular_speed_y = 0
        self.angular_speed_z = 0

        self.acceleration_x = 0
        self.acceleration_y = 0
        self.acceleration_z = 0

        self.magnetic_field_x = 0
        self.magnetic_field_y = 0
        self.magnetic_field_z = 0

        self.altitude = 0

        self.latitude = 0
        self.longitude = 0

        self.temperature_1 = 0

        self.stress_1 = 0

    def upadate_data(self, data_buffer):
        """
        Update RocketData attributes from data_buffer
        :param data_buffer: String d'octets
        """

        data_array = struct.unpack_from(self.DATA_FORMAT,data_buffer)
    
class RocketPacket:
    def __init__(self):
        self.rocket_data = RocketData()
        self.crc32 = 0
        
    
