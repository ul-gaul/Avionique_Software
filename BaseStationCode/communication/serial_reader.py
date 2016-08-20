from threading import Thread
from serial import Serial
from communication.DetectSerial import serial_port
from rocket_data.rocket_packet import RocketData


class AcquisitionThread(Thread):
    BAUDRATE = 57600
    START_CHARACTER = b's'
    PACKET_SIZE = 69

    def __init__(self, acquisition_queue):
        super(AcquisitionThread, self).__init__()
        self.acquisition_queue = acquisition_queue
        port_nb = serial_port()[0]
        self.device = Serial(port_nb, baudrate=self.BAUDRATE, timeout=0.2)
        self.exit_flag = False

    def run(self):
        while not self.exit_flag:
            c = self.device.read(1)
            if c == self.START_CHARACTER:
                while self.device.inWaiting() < self.PACKET_SIZE:
                    pass
                data = self.device.read(self.PACKET_SIZE)

                rocket_data = RocketData(data)
                # checksum_validated = rocket_data.validateCheckSum()
                checksum_validated = True
                if checksum_validated:
                    self.acquisition_queue.put(rocket_data)

    def stop(self):
        self.exit_flag = True

