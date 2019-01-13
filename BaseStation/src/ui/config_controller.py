import configparser


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

    def get_sections(self):
        return self.config.sections()

    def get_settings(self, section_name=None):
        try:
            return self.config[section_name].items()
        except KeyError:
            return []

    @staticmethod
    def _infer_type(value_str):
        """Deviner le type de la valeur selon une certaine heuristique"""
        pass
