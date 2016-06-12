__author__ = 'Maxime'

import time
import serial
import sys
import threading
import numpy as np
import csv
from BaseStationCode.rocket_data.rocket_packet import RocketData
from BaseStationCode.communication.DetectSerial import serial_port
import datetime


class SerialReader(threading.Thread):

    def __init__(self, port, csv_file):
        super(SerialReader, self).__init__()
        self.RocketDataList = []
        self.port = port

        self.csvFile = open(csv_file, 'w',  newline= '')
        self.writer = csv.writer(self.csvFile)
        self.writer.writerow(["Starting new data acquisition : " + str(datetime.datetime.now()), None])

        self.exitFlag = False
        self.exitMutex = threading.Lock()
        self.dataMutex = threading.Lock()

    def run(self):
        while True:
            # check if exit was requested
            if self.exitFlag:
                self.csvFile.close()
                self.port.close()
                break

            while(self.port.inWaiting() < 68):
                pass

            # read data from the serial port
            data = self.port.readline()
            #print(data)
            RData = RocketData(data)

            #checksum
            if(RData.validateCheckSum()):
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

if __name__ == "__main__":
    portNumber = serial_port()[0]
    port = serial.Serial(portNumber, 9600,timeout = 0.2)
    reader = SerialReader(port, "../acquisition.csv")
    reader.start()
    time.sleep(2)
    list = reader.get()
    print(list[0].angular_speed_x)
    reader.exit()
