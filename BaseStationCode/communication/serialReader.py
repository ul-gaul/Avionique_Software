__author__ = 'Maxime'

import time
import serial
import sys
import threading
import numpy as np
import csv
from ..rocket_data.rocket_packet import RocketData


class SerialReader(threading.Thread):

    def init(self, port, csv_file):
        threading.Thread.__init__(self)
        self.RocketDataList = []
        self.port = port

        self.csvFile = open(csv_file, 'w',  newline= '')
        self.writer = csv.writer(self.csvFile)

        self.exitFlag = False
        self.exitMutex = threading.Lock()
        self.dataMutex = threading.Lock()

    def run(self):
        while True:
            # check if exit was requested
            if self.exitFlag:
                self.csvFile.close()
                break

            # read data from the serial port
            data = self.port.readline()
            RData = RocketData(data)

            #checksum
            if(RData.checkSum()):
                with self.dataMutex:
                    self.RocketDataList.append(RData)
                self.writer.writerow([RData.timeStamp, RData.angular_speed_x, RData.angular_speed_y, RData.angular_speed_z, RData.acceleration_x, RData.acceleration_y, RData.acceleration_z, RData.magnetic_field_x, RData.magnetic_field_y, RData.magnetic_field_z, RData.altitude, RData.latitude_1, RData.longitude_1, RData.latitude_2, RData.longitude_2, RData.temperature_1, RData.temperature_2] + [None])

    def get(self):
        with self.dataMutex:
            tmp = self.RocketDataList
            self.RocketDataList = []
            return tmp

    def exit(self):
        with self.exitMutex:
            self.exitFlag = True
