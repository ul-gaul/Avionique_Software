import glob
import struct
import sys
import threading

import serial

from src.data_persister import DataPersister
from src.data_producer import DataProducer
from src.realtime.checksum_validator import ChecksumValidator
from src.realtime.rocket_packet_parser import RocketPacketParser


class NoConnectedDeviceException(Exception):
    """Raised when data acquisition is started with no device connected"""


class SerialDataProducer(DataProducer):

    def __init__(self, lock: threading.Lock, data_persister: DataPersister, rocket_packet_parser: RocketPacketParser,
                 checksum_validator: ChecksumValidator, baudrate=9600, start_character=b's', sampling_frequency=1.0):
        super().__init__(lock)
        self.data_persister = data_persister
        self.rocket_packet_parser = rocket_packet_parser
        self.checksum_validator = checksum_validator
        self.unsaved_data = False

        self.port = serial.Serial()
        self.port.baudrate = baudrate
        self.port.timeout = 1 / sampling_frequency
        self.start_character = start_character

        # RocketPacket data + 1 byte for checksum
        self.num_bytes_to_read = self.rocket_packet_parser.get_number_of_bytes() + 1

    def start(self):
        ports = self.detect_serial_ports()
        if not ports:
            raise NoConnectedDeviceException("Aucun récepteur connecté")
        self.port.port = ports[0]
        self.port.open()

        self.is_running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        while self.is_running:
            c = self.port.read(1)
            if c == self.start_character:
                data_bytes = self.port.read(self.num_bytes_to_read)

                if self.checksum_validator.validate(data_bytes):
                    try:
                        rocket_packet = self.rocket_packet_parser.parse(data_bytes[:-1])
                        print(rocket_packet)
                        self.add_rocket_packet(rocket_packet)
                        self.unsaved_data = True
                    except struct.error:
                        """
                        This error can occur if we don't read enough bytes on the serial port or if the packet format is
                        incorrect.
                        """
                        print("Invalid packet")
        self.port.close()

    def save(self, filename: str):
        self.data_persister.save(filename, self.available_rocket_packets)
        self.unsaved_data = False

    def has_unsaved_data(self):
        return self.unsaved_data

    def clear_rocket_packets(self):
        self.lock.acquire()
        self.available_rocket_packets.clear()
        self.unsaved_data = False
        self.lock.release()

    @staticmethod
    def detect_serial_ports():
        """ Lists serial port names
        :raises EnvironmentError
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
        """

        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
