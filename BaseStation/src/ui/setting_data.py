class SettingData:
    """Représente un paramètre de configuration de l'application"""

    def __init__(self, name, value=None, input_type='text', choices=None, label=None, section=None, parsed=True):
        self.name = name
        self.value = value
        self.type = input_type
        self.choices = choices
        self.label = label
        self.section = section
        self.parsed = parsed

        def __key__(self):
            return (self.section, self.name)

        def __hash__(self):
            return hash(self.__key__())

        def __lt__(self, other):
            return self.__key__() < other.__key__()
