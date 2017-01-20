from threading import Thread
from serial import Serial
from rocket_data.rocket_packet import RocketPacket
from src.producer import Producer
import sys
import glob
import serial


class SerialReader(Producer):
    PACKET_SIZE = 69

    def __init__(self, baudrate=9600, start_character=b's'):
        super().__init__()
        self.port = Serial()
        self.port.baudrate = baudrate
        self.port.timeout = 0.2
        self.start_character = start_character
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
                while self.port.inWaiting() < self.PACKET_SIZE:
                    pass
                data = self.port.read(self.PACKET_SIZE)

                rocket_packet = RocketPacket(data)
                if rocket_packet.validate_checksum():
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
