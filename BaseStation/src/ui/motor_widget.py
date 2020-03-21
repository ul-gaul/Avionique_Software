from PyQt5.uic.properties import QtWidgets

from src.ui.data_motorwidget import DataMotorWidget


class MotorWidget(DataMotorWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_valve_pushButton_clicked = []
        self.callbacks = {}

        self.register_all_valve_pushButton()

    def set_callback(self, name, func):
        self.callbacks.update({name: func})

    # Ajouter piston.
    # Essayer de le moduler pour run en command line.
    # Coder de quoi envoyer des commandes.
    # Coder de quoi recevoir une verification de commandes.
    # comm module.
    def valve_pushButton_on_click(self, index: int, button):
        if not self.is_valve_pushButton_clicked[index]:
            self.is_valve_pushButton_clicked[index] = True
            self.set_valve_pushButton_on(button)
        else:
            self.is_valve_pushButton_clicked[index] = False
            self.set_valve_pushButton_off(button)

    def register_all_valve_pushButton(self):
        self.register_valve_pushButton(self.valve_pushButton_1)
        self.register_valve_pushButton(self.valve_pushButton_2)
        self.register_valve_pushButton(self.valve_pushButton_3)
        self.register_valve_pushButton(self.valve_pushButton_4)
        self.register_valve_pushButton(self.valve_pushButton_5)

    def register_valve_pushButton(self, button):
        self.is_valve_pushButton_clicked.append(False)
        button.clicked.connect(lambda: self.valve_pushButton_on_click(len(self.is_valve_pushButton_clicked) - 1, button))

    def reset(self):
        super().reset()
