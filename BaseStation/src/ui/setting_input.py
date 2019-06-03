class SettingInput:
    """
    Interface qui représente un champ de configuration dans un projet Qt
    """

    def __init__(self, name, *args, **kwargs):
        self.name = name

    def get_value(self):
        """Retourne la valeur actuelle du champ"""
        raise NotImplementedError

    def get_name(self):
        """Retourne le nom du champ"""
        return self.name

    def qt(self):
        """Retourne un widget Qt qui affiche le champ"""
        return self._widget
