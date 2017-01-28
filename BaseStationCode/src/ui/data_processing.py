import numpy as np
from collections import deque
from math import sqrt


class DataProcessing:
    def __init__(self, ):
        self.split_data = {}
        # TODO : use collections.deque instead of list to always have the same number of points in each vector
        self.split_data["time"] = []
        self.split_data["accx"] = []
        self.split_data["accy"] = []
        self.split_data["accz"] = []
        self.split_data["angx"] = []
        self.split_data["angy"] = []
        self.split_data["angz"] = []
        self.split_data["magx"] = []
        self.split_data["magy"] = []
        self.split_data["magz"] = []
        self.split_data["alt"] = []
        self.split_data["lat1"] = []
        self.split_data["lat2"] = []
        self.split_data["long1"] = []
        self.split_data["long2"] = []
        self.split_data["temp1"] = []
        self.split_data["temp2"] = []
        self.split_data["verticalSpeed"] = []
        self.split_data["meanlat"] = []
        self.split_data["meanlong"] = []

        self.acc = []
        self.acheckpoint = 0

    def add_data(self, rocket_data):
        self.split_data["time"].append(rocket_data.time_stamp)
        self.split_data["accx"].append(-rocket_data.acceleration_x)
        self.split_data["accy"].append(rocket_data.acceleration_y)
        self.split_data["accz"].append(rocket_data.acceleration_z)
        self.split_data["angx"].append(rocket_data.angular_speed_x)
        self.split_data["angy"].append(rocket_data.angular_speed_y)
        self.split_data["angz"].append(rocket_data.angular_speed_z)
        self.split_data["magx"].append(rocket_data.magnetic_field_x)
        self.split_data["magy"].append(rocket_data.magnetic_field_y)
        self.split_data["magz"].append(rocket_data.magnetic_field_z)
        self.split_data["alt"].append(rocket_data.altitude)
        self.split_data["lat1"].append(rocket_data.latitude_1)
        self.split_data["lat2"].append(rocket_data.latitude_2)
        self.split_data["long1"].append(rocket_data.longitude_1)
        self.split_data["long2"].append(rocket_data.longitude_2)
        self.split_data["temp1"].append(rocket_data.temperature_1)
        self.split_data["temp2"].append(rocket_data.temperature_2)

        self.split_data["meanlat"].append((rocket_data.latitude_1 + rocket_data.latitude_2) / 2)
        self.split_data["meanlong"].append((rocket_data.longitude_1 + rocket_data.longitude_2) / 2)

        if len(self.split_data["alt"]) == 1:
            self.split_data["verticalSpeed"].append(0)
        if len(self.split_data["alt"]) > 1:
            self.split_data["verticalSpeed"].append((self.split_data["alt"][-1] - self.split_data["alt"][-2]) / (self.split_data["time"][-1] - self.split_data["time"][-2]))

    def acc_normalisation(self):
        if len(self.data["accx"]) == len(self.data["accy"]) and len(self.data["accx"]) == len(self.data["accz"]):

            for j in range(len(self.data["accx"])):
                self.acc.append(sqrt((self.data["accx"][j+self.acheckpoint]**2)+(self.data["accy"][j+self.acheckpoint]**2)+(self.data["accz"][j+self.acheckpoint]**2)))
            self.acheckpoint = len(self.data["accx"])
