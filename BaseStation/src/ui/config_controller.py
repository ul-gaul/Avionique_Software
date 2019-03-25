import configparser
import sys
import glob
import serial
import serial.tools.list_ports

from src.ui.config_validator import ConfigValidator


class ConfigController:
    def __init__(self, chemin_fichier):
        self.file_path = chemin_fichier
        self.validator = ConfigValidator()
        self.config = configparser.ConfigParser()
        self.config.read(self.file_path)

    @staticmethod
    def _get_value(input_el, input_type):
        if input_type.endswith('list'):
            if input_el.currentItem() is None:
                return None
            return input_el.currentItem().text()
        return input_el.text()

    def save_to_file(self):
        with open(self.file_path, 'w') as f:
            self.config.write(f)

    def save(self, inputs, on_input_error, onsuccess, onerror):
        success = True
        for name, inputItem in inputs.items():
            value = self._get_value(inputItem["input"], inputItem["type"])
            if value is None:
                continue
            error = self.validator.get_errors({name: value})
            if not error:
                self.set_value(inputItem["section"], name, value)
            else:
                success = False
                on_input_error(inputItem['label'], error[name])
        if success:
            self.save_to_file()
            onsuccess()
        else:
            onerror()

    def set_value(self, section, name, value):
        self.config[section][name] = value

    def get_value(self, section, name):
        return self.config[section][name]

    def get_parsed_sections(self):
        return self.config.sections()

    def get_sections(self):
        return set(list(self.get_parsed_sections() + self.get_dynamic_sections()))

    def get_settings(self, section_name=None):
        settings = []
        if section_name in self.get_parsed_sections():
            settings += [
                (name, (value, 'edit', None)) for (name, value) in self.config[section_name].items()]
        if self.get_dynamic_settings(section_name):
            parsed_end = len(settings)
            parsed_names = [name for (name, _) in settings[:parsed_end]]
            settings += self.get_dynamic_settings(section_name)
            for (name, _) in settings[parsed_end:]:
                try:
                    doublon_pos = parsed_names.index(name)
                except ValueError:
                    continue
                else:
                    settings.remove(settings[doublon_pos])
            print(settings)
        return settings

    def get_dynamic_sections(self):
        return ['serial_port']

    def get_dynamic_settings(self, section_name):
        settings = {
            'serial_port': [
                ('port_com', (self._get_serial_port_options(), 'list', 'Port COM'))],
            'general': [
                ('language', (['EN', 'FR'], 'list', 'Langue'))],
            'rocket_packet': [
                ('version', (['2018', '2019'], 'list', 'Version RocketPaquet'))]
        }
        return settings.get(section_name, [])

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
            ports = [p[0] for p in serial.tools.list_ports.comports()]
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
                s = serial.Serial(port, timeout=0)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
