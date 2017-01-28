import glob
import sys
import struct
import serial
from threading import Thread

from src.producer import Producer
from src.rocket_packet import RocketPacket


class SerialReader(Producer):
    def __init__(self, baudrate=9600, start_character=b's', packet_size=121,
                 packet_format="<fffffffffffffffffffffffBBBBBBfffffBBB"):
        super().__init__()
        self.port = serial.Serial()
        self.port.baudrate = baudrate
        self.port.timeout = 0.2

        # TODO: a confirmer avec l'equipe d'acquisition
        self.start_character = start_character
        self.packet_size = packet_size
        self.format = packet_format

        self.flightData = []
        self.thread = Thread(target=self.run)

    def start(self):
        self.port.port = self.detect_serial()[0]
        self.port.open()
        self.is_running = True
        self.thread.start()

    def run(self):
        while self.is_running:
            c = self.port.read(1)
            if c == self.start_character:
                # FIXME: peut creer une boucle infinie lors de l'arret de la transmission
                while self.port.inWaiting() < self.packet_size:
                    pass

                data_array = self.port.read(self.packet_size)
                tmp_list = struct.unpack(self.format, data_array)
                data_list = tmp_list[:-1]
                checksum = tmp_list[-1]

                if self.validate_checksum(data_array[:-1], checksum):
                    rocket_packet = RocketPacket(data_list)
                    self.rocket_packets.put(rocket_packet)
                    # TODO: decider si on ecrit dans le csv seulement a la fin, ou au fur et a mesure
                    self.flightData.append(rocket_packet)
        self.port.close()

    def stop(self):
        super().stop()
        # TODO: save dans le fichier csv avec le module de sauvegarde

    @staticmethod
    def detect_serial():
        """ Lists serial port names
        :raises EnvironmentError
            On unsopported or unknown platforms
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

    @staticmethod
    def validate_checksum(data_array, expected_checksum):
        # TODO: s'entendre avec l'equipe d'acquisition pour la formule a utiliser
        checksum = sum(data_array[0:-1]) % 256
        if checksum == expected_checksum:
            return True
        else:
            print("Invalid Checksum : expected = {}, calculated = {}".format(expected_checksum, checksum))
            return False
