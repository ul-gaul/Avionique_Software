# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 12:03:00 2016

@author: Maxime
"""
import struct


class RocketData:
    def __init__(self, data_buffer):
        self.format = "<fffffffffffffffffB"
        self.data_buffer = data_buffer
        # print(len(data_buffer))
        newData = struct.unpack(self.format, data_buffer)

        self.time_stamp = newData[0]

        self.angular_speed_x = newData[1]
        self.angular_speed_y = newData[2]
        self.angular_speed_z = newData[3]

        self.acceleration_x = newData[4]
        self.acceleration_y = newData[5]
        self.acceleration_z = newData[6]

        self.magnetic_field_x = newData[7]
        self.magnetic_field_y = newData[8]
        self.magnetic_field_z = newData[9]

        self.altitude = newData[10]

        self.latitude_1 = newData[11]
        self.longitude_1 = newData[12]
        self.latitude_2 = newData[13]
        self.longitude_2 = newData[14]

        self.temperature_1 = newData[15]
        self.temperature_2 = newData[16]

        self.checkSum = newData[17]

    def validateCheckSum(self):
        checkSum = sum(self.data_buffer[0:-2])%256
        if checkSum == self.checkSum:
            return True
        else:
            print("Invalid Checksum : data = {}, calculated = {}".format(self.checkSum, checkSum))
            return False


    def print_data(self):
        print("Time Stamp = {}".format(self.time_stamp))

        print("Ang Speed X = {}".format(self.angular_speed_x))
        print("Ang Speed Y = {}".format(self.angular_speed_y))
        print("Ang Speed Z = {}".format(self.angular_speed_z))

        print("Accel X = {}".format(self.acceleration_x))
        print("Accel Y = {}".format(self.acceleration_y))
        print("Accel Z = {}".format(self.acceleration_z))

        print("Magnet X = {}".format(self.magnetic_field_x))
        print("Magnet Y = {}".format(self.magnetic_field_y))
        print("Magnet Z = {}".format(self.magnetic_field_z))

        print("Altitude = {}".format(self.altitude))

        print("Latitude 1 = {}".format(self.latitude_1))
        print("Longitude 1 = {}".format(self.longitude_1))
        print("Latitude 2 = {}".format(self.latitude_2))
        print("Longitude 2 = {}".format(self.longitude_2))

        print("Temp 1 = {}".format(self.temperature_1))
        print("Temp 2 = {}".format(self.temperature_2))

        print("Checksum = {}\n\n".format(self.checkSum))


if __name__ == "__main__":
    pass
