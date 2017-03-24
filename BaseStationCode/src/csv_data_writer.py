import csv
import os
from datetime import datetime as d
from PyQt5.QtWidgets import (QApplication, QWidget,  QSizePolicy, QSpacerItem, QFileDialog, QTextEdit, QVBoxLayout, QPushButton, QHBoxLayout, QTextBrowser, )
#from ..rocket_data import rocket_packet
from PyQt5.QtGui import QIcon
import sys

class CsvDataWriter(QWidget):

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

    def __init__(self, parent=None):

        super().__init__(parent=parent)
        self.initUI()

    def initUI(self):

        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout()
        self.textBrowser = QTextBrowser(self)
        self.textBrowser.setFontPointSize(7)
        save_btn = QPushButton("Save", self)
        save_btn.clicked.connect(self.saveCSV)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        vbox.addItem(spacerItem)
        #self.textBrowser.insertPlainText((", ".join(self.HEADER_FIELDS)))
        #for num in range(len(self.HEADER_FIELDS)):
            #self.textBrowser.insertPlainText(", " + self.HEADER_FIELDS[num])
        vbox.addWidget((self.textBrowser))
        spacerItem1 = QSpacerItem(10,20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        hbox.addItem(spacerItem1)
        hbox.addWidget(save_btn)
        vbox.addLayout(hbox)

        self.setGeometry(300, 300, 1085, 250)
        self.setWindowTitle("Rocket Packet Preview")


    def saveCSV(self):

        self.filename, _ = QFileDialog.getSaveFileName(self, "Save File",
        d.now().strftime("%Y-%m-%d_%Hh%M")+".csv", "All Files (*);; CSV Files (*.csv)")
        if self.filename:
            print("Saved %s in %s" % (d.now().strftime("%Y-%m-%d_%Hh%M")+".csv",
                  self.filename))
            with open(self.filename, "w") as file:
                self.write_header()
                #self.write_line()
                self.filename.close()

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
"""For testing purpose"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    f = CsvDataWriter()
    f.show()
    sys.exit(app.exec_())








