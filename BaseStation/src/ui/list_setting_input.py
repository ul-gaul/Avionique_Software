from PyQt5.QtWidgets import QListWidget

from .setting_input import SettingInput


class ListSettingInput(SettingInput):
    """Champ de sélection dans une liste de configuration"""

    def __init__(self, name, options, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self._widget = QListWidget(*args, **kwargs)
        self._widget.addItems(options)

    def get_value(self):
        try:
            return self._widget.currentItem().text()
        except AttributeError:
            return ''
