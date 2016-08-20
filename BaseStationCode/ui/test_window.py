from PyQt4 import QtGui, QtCore
from queue import Queue, Empty

from communication.serial_reader import AcquisitionThread
from rocket_data.csv_data_writer import CsvDataWriter
from ui.test_windowUI import Ui_TestWindow
from rocket_data.rocket_packet import RocketData


class HandlingDataThread(QtCore.QThread):
    data_received = QtCore.pyqtSignal(RocketData)

    def __init__(self, acquisition_queue):
        QtCore.QThread.__init__(self)
        self.acquisition_queue = acquisition_queue
        self.exit_flag = True

    def run(self):
        self.exit_flag = False
        csv_writer = CsvDataWriter()
        while not self.exit_flag:
            try :
                rocket_data = self.acquisition_queue.get(block=False, timeout=2)
                # rocket_data.print_data()
                csv_writer.write_line(rocket_data)
                self.data_received.emit(rocket_data)
            except Empty:
                pass

    def stop(self):
        self.exit_flag = True


class TestWindow(QtGui.QMainWindow, Ui_TestWindow):
    def __init__(self, parent):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(parent)
        self.queue = Queue(maxsize=1000000)

        self.handling_data_thread = HandlingDataThread(self.queue)
        self.acquisition_thread = AcquisitionThread(self.queue)

        self.init_widgets()
        self.link_widgets()


        self.vertical_speed = 0
        self.last_altitude = 0 # used to calculate vertical speed
        self.last_time_stamp = 0 # used to calculate vertical speed
        self.max_altitude = 0

    def init_widgets(self):
        self.stop_button.setEnabled(False)

    def link_widgets(self):
        self.start_button.clicked.connect(self.start_acquisition)
        self.stop_button.clicked.connect(self.stop_acquisition)
        self.handling_data_thread.data_received.connect(self.update_lcds)

    def start_acquisition(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.handling_data_thread.start()
        self.acquisition_thread.start()

    def stop_acquisition(self):
        self.handling_data_thread.stop()
        self.acquisition_thread.stop()
        self.stop_button.setEnabled(False)

    def update_lcds(self, rocket_data):
        # Calculate vertical speed and max altitude
        self.vertical_speed = 3.6*(rocket_data.altitude - self.last_altitude)/\
                              (rocket_data.time_stamp - self.last_time_stamp)
        self.last_altitude = rocket_data.altitude
        self.last_time_stamp = rocket_data.time_stamp
        self.max_altitude = max([self.max_altitude, rocket_data.altitude])

        # update lcds
        self.time_lcd.display("{:.2f}".format(rocket_data.time_stamp))
        self.speed_lcd.display("{:.2f}".format(self.vertical_speed))
        self.altitude_lcd.display("{:.1f}".format(rocket_data.altitude))
        self.max_altitude_lcd.display("{:.1f}".format(self.max_altitude))
        self.acceleration_z_lcd.display("{:.1f}".format(rocket_data.acceleration_x))
        self.temperature_lcd.display("{:.1f}".format(rocket_data.temperature_1))
        self.latitude_lcd.display("{:.6f}".format(rocket_data.latitude_1))
        self.longitude_lcd.display("{:.6f}".format(rocket_data.longitude_1))

    def closeEvent(self, event):
        print("close event")
        self.stop_acquisition()
        super(TestWindow, self).closeEvent(event)





