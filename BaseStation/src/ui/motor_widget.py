from src.ui.data_motor_window import DataMotorWindow


class MotorWidget(DataMotorWindow):

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
            self.set_valve_pushButton_wait(button)
        else:
            self.is_valve_pushButton_clicked[index] = False
            self.set_valve_pushButton_off(button)

        if index == 0:
            self.callbacks["send_cmd_valve_1"]()
        elif index == 1:
            self.callbacks["send_cmd_valve_2"]()
        elif index == 2:
            self.callbacks["send_cmd_valve_3"]()
        elif index == 3:
            self.callbacks["send_cmd_valve_4"]()
        elif index == 4:
            self.callbacks["send_cmd_valve_5"]()

    def register_all_valve_pushButton(self):
        self.register_valve_pushButton(0, self.valve_pushButton_1)
        self.register_valve_pushButton(1, self.valve_pushButton_2)
        self.register_valve_pushButton(2, self.valve_pushButton_3)
        self.register_valve_pushButton(3, self.valve_pushButton_4)
        self.register_valve_pushButton(4, self.valve_pushButton_5)

    def register_valve_pushButton(self, index, button):
        self.is_valve_pushButton_clicked.append(False)
        button.clicked.connect(lambda: self.valve_pushButton_on_click(index, button))

    def getButtonByCommandID(self, cmd_id: int):
        if cmd_id == 1:
            return self.valve_pushButton_1
        elif cmd_id == 2:
            return self.valve_pushButton_2
        elif cmd_id == 3:
            return self.valve_pushButton_3
        elif cmd_id == 4:
            return self.valve_pushButton_4
        elif cmd_id == 5:
            return self.valve_pushButton_5

    def reset(self):
        super().reset()
