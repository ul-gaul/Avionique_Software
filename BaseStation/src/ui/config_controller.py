import configparser
import sys
import glob
import serial

from src.ui.setting_data import SettingData


class ConfigController:
    def __init__(self, chemin_fichier):
        self.file_path = chemin_fichier
        self.config = configparser.ConfigParser()
        self.config.read(self.file_path)

    def save_to_file(self):
        with open(self.file_path, 'w') as f:
            self.config.write(f)

    def set_value(self, section, name, value):
        self.config[section][name] = value

    def get_value(self, section, name):
        return self.config[section][name]

    def get_parsed_sections(self):
        return self.config.sections()

    def get_sections(self):
        return set(self.get_parsed_sections() + self.get_dynamic_sections())

    def get_settings(self, section=None):
        settings = {}
        if section in self.get_parsed_sections():
            settings = {
                name: SettingData(name, value, section=section) for (name, value) in self.config[section].items()
            }
        if section in self.get_dynamic_sections():
            settings.update(self.get_dynamic_settings(section))
        return settings.values()

    def get_dynamic_sections(self):
        return ['serial_port']

    def get_dynamic_settings(self, section_name):
        settings = {'serial_port': {
            'port_com': SettingData('port_com', input_type='list', choices=self._get_serial_port_options(), section='serial_port')
        }}
        return settings.get(section_name)

    def _get_serial_port_options(self):
        return self.detect_serial_ports()

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
