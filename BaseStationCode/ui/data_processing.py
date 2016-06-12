import numpy as np
from math import sqrt
from BaseStationCode.communication.serialReader import SerialReader as SR
from BaseStationCode.rocket_data.rocket_packet import RocketData as RD


class DataProcessing:

    def __init__(self):
        self.data = {}
        self.data["time"] = []
        self.data["accx"] = []
        self.data["accy"] = []
        self.data["accz"] = []
        self.data["angx"] = []
        self.data["angy"] = []
        self.data["angz"] = []
        self.data["magx"] = []
        self.data["magy"] = []
        self.data["magz"] = []
        self.data["alt"] = []
        self.data["lat1"] = []
        self.data["lat2"] = []
        self.data["long1"] = []
        self.data["long2"] = []
        self.data["temp1"] = []
        self.data["temp2"] = []

        self.acc = []
        self.speed = [0]
        self.acccheckpoint = 0


    def fetch_data(self):
        self.dataliste = SR.get()

        for j in range(len(self.dataliste)):
            self.data["time"].append(self.dataliste[j].timeStamp)
            self.data["accx"].append(self.dataliste[j].acceleration_x)
            self.data["accy"].append(self.dataliste[j].acceleration_y)
            self.data["accz"].append(self.dataliste[j].acceleration_z)
            self.data["angx"].append(self.dataliste[j].angular_speed_x)
            self.data["angy"].append(self.dataliste[j].angular_speed_y)
            self.data["angz"].append(self.dataliste[j].angular_speed_z)
            self.data["magx"].append(self.dataliste[j].magnetic_field_x)
            self.data["magz"].append(self.dataliste[j].magnetic_field_z)
            self.data["alt"].append(self.dataliste[j].altitude)
            self.data["lat1"].append(self.dataliste[j].latitude_1)
            self.data["lat2"].append(self.dataliste[j].latitude_2)
            self.data["long1"].append(self.dataliste[j].longitude_1)
            self.data["long2"].append(self.dataliste[j].longitude_2)
            self.data["temp1"].append(self.dataliste[j].temperature_1)
            self.data["temp2"].append(self.dataliste[j].temperature_2)
            """self.data["time"].append(RD.timeStamp)
            self.data["accx"].append(RD.acceleration_x)
            self.data["accy"].append(RD.acceleration_y)
            self.data["accz"].append(RD.acceleration_z)
            self.data["angx"].append(RD.angular_speed_x)
            self.data["angy"].append(RD.angular_speed_y)
            self.data["angz"].append(RD.angular_speed_z)
            self.data["magx"].append(RD.magnetic_field_x)
            self.data["magy"].append(RD.magnetic_field_y)
            self.data["magz"].append(RD.magnetic_field_z)
            self.data["alt"].append(RD.altitude)
            self.data["lat1"].append(RD.latitude_1)
            self.data["lat2"].append(RD.latitude_2)
            self.data["long1"].append(RD.longitude_1)
            self.data["long2"].append(RD.longitude_2)
            self.data["temp1"],append(RD.temperature_1)
            self.data["temp2"].append(RD.temperature_2)"""

        self.dataliste = []

    def acc_normalisation(self):
        if len(self.data["accx"]) == len(self.data["accy"]) and len(self.data["accx"]) == len(self.data["accz"]):

            for j in range(len(self.data["accx"])):
                self.acc.append(sqrt((self.data["accx"][j]**2)+(self.data["accy"][j]**2)+(self.data["accz"][j]**2)))
                self.acccheckpoint += 1

    def speed_norm(self):
        for j in range(len(self.acc)):
            self.speed.append(self.speed[j]+self.acc[j]*self.data["time"][j])

