import configparser
import sys
import glob
import serial


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
        return set(list(self.get_parsed_sections() + self.get_dynamic_sections()))

    def get_settings(self, section_name=None):
        settings = []
        if section_name in self.get_parsed_sections():
            settings += [
                (name, (value, 'edit', None)) for (name, value) in self.config[section_name].items()
                if name not in self.get_dynamic_sections()]
        if section_name in self.get_dynamic_sections():
            parsed_end = len(settings)
            parsed_names = [name for (name, _) in settings[:parsed_end]]
            settings += self.get_dynamic_settings(section_name)
            if len(settings) > parsed_end:
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
        settings = {'serial_port': [
            ('port_com', (self._get_serial_port_options(), 'list', 'Port COM'))]}
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

    @staticmethod
    def _infer_type(value_str):
        """Deviner le type de la valeur selon une certaine heuristique"""
        pass
