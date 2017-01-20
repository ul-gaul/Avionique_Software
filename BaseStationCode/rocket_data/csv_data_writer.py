import csv
import os
from datetime import datetime

from rocket_data.rocket_packet import RocketPacket


class CsvDataWriter:
    HEADER_FIELDS = ["TIME STAMP",
                     "ANG SPEED X",
                     "ANG SPEED Y",
                     "ANG SPEED Z",
                     "ACCEL X",
                     "ACCEL Y",
                     "ACCEL Z",
                     "MAGNET X",
                     "MAGNET Y",
                     "MAGNET Z",
                     "ALTITUDE",
                     "LATITUDE 1",
                     "LONGITUDE 1",
                     "LATITUDE 2",
                     "LONGITUDE 2",
                     "TEMPERATURE 1",
                     "TEMPERATURE 2"]

    def __init__(self):
        self.filename = os.path.join("output_files",
                                     "{}_acquisition_data.csv".format(datetime.now().strftime("%Y%m%d_%H%M%S")))
        self.write_header()

    def write_header(self):
        with open(self.filename, 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file,
                                    fieldnames=self.HEADER_FIELDS,
                                    delimiter=',')
            writer.writeheader()

    def write_line(self, rocket_data):
        with open(self.filename, 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file,
                                    fieldnames=self.HEADER_FIELDS,
                                    delimiter=',')
            writer.writerow({"TIME STAMP" : rocket_data.time_stamp,
                             "ANG SPEED X" : rocket_data.angular_speed_x,
                             "ANG SPEED Y" : rocket_data.angular_speed_y,
                             "ANG SPEED Z" : rocket_data.angular_speed_z,
                             "ACCEL X" : rocket_data.acceleration_x,
                             "ACCEL Y" : rocket_data.acceleration_y,
                             "ACCEL Z" : rocket_data.acceleration_z,
                             "MAGNET X" : rocket_data.magnetic_field_x,
                             "MAGNET Y" : rocket_data.magnetic_field_y,
                             "MAGNET Z" : rocket_data.magnetic_field_z,
                             "ALTITUDE" : rocket_data.altitude,
                             "LATITUDE 1" : rocket_data.latitude_1,
                             "LONGITUDE 1" : rocket_data.longitude_1,
                             "LATITUDE 2" : rocket_data.latitude_2,
                             "LONGITUDE 2" : rocket_data.longitude_2,
                             "TEMPERATURE 1" : rocket_data.temperature_1,
                             "TEMPERATURE 2" : rocket_data.temperature_2})

