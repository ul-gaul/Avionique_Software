import numpy as np
from math import sqrt


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
        self.acheckpoint = 0

    def add_data(self, dataList):
        for j in range(len(dataList)):
            self.data["time"].append(dataList[j].timeStamp)
            self.data["accx"].append(dataList[j].acceleration_x)
            self.data["accy"].append(dataList[j].acceleration_y)
            self.data["accz"].append(dataList[j].acceleration_z)
            self.data["angx"].append(dataList[j].angular_speed_x)
            self.data["angy"].append(dataList[j].angular_speed_y)
            self.data["angz"].append(dataList[j].angular_speed_z)
            self.data["magx"].append(dataList[j].magnetic_field_x)
            self.data["magy"].append(dataList[j].magnetic_field_y)
            self.data["magz"].append(dataList[j].magnetic_field_z)
            self.data["alt"].append(dataList[j].altitude)
            self.data["lat1"].append(dataList[j].latitude_1)
            self.data["lat2"].append(dataList[j].latitude_2)
            self.data["long1"].append(dataList[j].longitude_1)
            self.data["long2"].append(dataList[j].longitude_2)
            self.data["temp1"].append(dataList[j].temperature_1)
            self.data["temp2"].append(dataList[j].temperature_2)

    def acc_normalisation(self):

        if len(self.data["accx"]) == len(self.data["accy"]) and len(self.data["accx"]) == len(self.data["accz"]):

            for j in range(len(self.data["accx"])):
                self.acc.append(sqrt((self.data["accx"][j+self.acheckpoint]**2)+(self.data["accy"][j+self.acheckpoint]**2)+(self.data["accz"][j+self.acheckpoint]**2)))
            self.acheckpoint = len(self.data["accx"])

    def speed_norm(self):
        for j in range(len(self.acc)):
            self.speed.append(self.speed[j]+self.acc[j]*self.data["time"][j])
