import serial
import serial.tools.list_ports
import struct


class SerialCommandSender:

    def __init__(self, port: str, baudrate: int, packet_format=None):
        self.serial = serial.Serial()
        self.set_port_and_baudrate(port, baudrate)
        self.packet_format = packet_format

    def set_port_and_baudrate(self, port: str, baudrate: int):
        if port not in self.get_all_opened_ports():
            #raise Exception("Le port specifer n'est pas existant")
            pass

        self.close_port()

        self.serial.port = port
        self.serial.baudrate = baudrate

    def set_command_format(self, cmd_format: str):
        self.packet_format = cmd_format

    def close_port(self):
        if self.serial.isOpen():
            self.serial.close()

    def open_port(self):
        self.close_port()
        self.serial.open()

    @staticmethod
    def get_all_opened_ports() -> list:
        return [comport.device for comport in serial.tools.list_ports.comports()]

    def send_command(self, *args):
        if self.serial.isOpen():
            #CRC
            cmd = struct.pack(self.packet_format, args)
            self.serial.write(cmd)
