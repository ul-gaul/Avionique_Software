# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 12:03:00 2016

@author: Maxime
"""
import struct


class RocketData:


    def __init__(self, data_buffer):
        self.format = ">fffffffffffffffff"

        """
         Compute checksum
        """

        newData = struct.unpack(self.format, data_buffer)

        self.timeStamp = newData[0]

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

    def checkSum(self):
        return True

"""
>>>>>>> origin/fix_ui
class RocketPacket:
    def __init__(self):
        self.rocket_data = RocketData()
        self.crc32 = 0
<<<<<<< HEAD
        
    
=======
 """

if __name__ == "__main__":
    pass
