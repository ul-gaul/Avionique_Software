from PyQt5.QtWidgets import QLineEdit

from .setting_input import SettingInput


class LineSettingInput(SettingInput):
    """Champ texte de configuration"""

    def __init__(self, name, value=None, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self._widget = QLineEdit(value, *args, **kwargs)

    def get_value(self):
        return self._widget.text()
