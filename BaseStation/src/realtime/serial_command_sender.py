import threading

import serial
import serial.tools.list_ports
import struct

from src.data_producer import DataProducer
from src.events.event import Event


class SerialCommandSender(DataProducer):
    def __init__(self, serial_port: serial, packet_format=None):
        self.port = serial_port
        self.packet_format = packet_format

        self.commands_sent = []

    def get_serial_port(self):
        return self.port

    def set_command_format(self, cmd_format: str):
        self.packet_format = cmd_format

    @staticmethod
    def get_all_opened_ports() -> list:
        return [comport.device for comport in serial.tools.list_ports.comports()]

    def clear_rocket_packets(self):
        pass

    def send_command(self, *args):
        if self.port is not None and self.port.isOpen():
            cmd_id = str(args[2]) + str(args[3])
            #TODO: CRC
            if cmd_id not in self.commands_sent:
                if len(args) > 0:
                    cmd = struct.pack(self.packet_format, *args)
                    self.port.write(cmd)
                    self.commands_sent.append(cmd_id)

    def start(self):
        self.is_running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self): #TODO: Comment envoyer des info depuis arduino et comment les interpreter?
        while self.is_running:
            if self.port.isOpen():
                first = self.port.read(1)
                if first == b'a':
                    number_of_bytes = 12
                    data_bytes = self.port.read(number_of_bytes)
                    if len(data_bytes) == number_of_bytes: #TODO: Faire une sorte de module pour simplifier le tout. Comme le parser du rp.
                        data_list = struct.unpack('iii', data_bytes)
                        cmd_id = str(data_list[2]) + str(data_list[3])
                        if cmd_id in self.commands_sent:
                            self.commands_sent.remove(cmd_id)
                            Event("on_command_receive", cmd_id, data_list[4])
