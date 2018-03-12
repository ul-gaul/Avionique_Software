import glob
import sys
import struct
import serial
from threading import Thread

from src.domain_error import DomainError
from src.data_persister import DataPersister
from src.data_producer import DataProducer
from src.rocket_packet import RocketPacket


class SerialDataProducer(DataProducer):

    def __init__(self, data_persister: DataPersister, baudrate=57600, start_character=b's', sampling_frequency=1):
        super().__init__()
        self.data_persister = data_persister
        self.port = serial.Serial()
        self.port.baudrate = baudrate
        self.port.timeout = sampling_frequency
        self.start_character = start_character

        # RocketPacket data + 1 byte for checksum
        self.num_bytes_to_read = RocketPacket.size_in_bytes + 1
        self.format = RocketPacket.format + "B"

        self.flightData = []
        self.unsaved_data = False
        self.thread = Thread(target=self.run)

    def start(self):
        ports = self.detect_serial_ports()
        if len(ports) <= 0:
            raise DomainError("Aucun récepteur connecté")
        self.port.port = ports[0]
        self.port.open()
        self.is_running = True
        self.thread.start()

    def run(self):
        while self.is_running:
            c = self.port.read(1)
            if c == self.start_character:
                data_array = self.port.read(self.num_bytes_to_read)
                try:
                    data_list = struct.unpack(self.format, data_array)

                    if self.validate_checksum(data_array):
                        rocket_packet = RocketPacket(data_list[:-1])
                        print(rocket_packet)
                        self.rocket_packets.put(rocket_packet)
                        self.flightData.append(rocket_packet)
                        self.unsaved_data = True
                except struct.error:
                    """
                    This error can occur if we don't read enough bytes on the serial port or if the packet format is
                    incorrect.
                    """
                    print("Invalid packet")
        self.port.close()

    def save(self, filename: str):
        self.data_persister.save(filename, self.flightData)
        self.unsaved_data = False

    def has_unsaved_data(self):
        return self.unsaved_data

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

    # FIXME: extract to a Checksum class, implementing a ValidationStrategy interface
    @staticmethod
    def validate_checksum(data_array):
        checksum = sum(data_array) % 256
        if checksum == 255:
            return True
        else:
            print("Invalid Checksum : expected = 255, calculated = {}".format(checksum))
            return False
