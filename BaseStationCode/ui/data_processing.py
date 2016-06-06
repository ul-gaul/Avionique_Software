import numpy as np
from math import sqrt



class DataProcessing():

    def __init__(self):
        self.data = {"sp":[], "magn" : [], "geo":[], "accx": [],"accy":[],"accz":[], "temp":[], "alt":[]}
        self.acc = []
        self.speed = [0]
        self.timestamp = 0.200
    def acc_normalisation(self,i):
        for j in i:
            self.acc.append(sqrt((self.data["accx"][j]**2)+(self.data["accy"][j]**2)+(self.data["accz"][j]**2)))
    def speed_norm(self):
        for j in range(len(self.acc)):
            self.speed.append(self.speed[j]+self.acc[j]*self.timestamp)
