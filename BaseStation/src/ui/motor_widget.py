from src.ui.data_motor_widget import DataMotorWidget


class MotorWidget(DataMotorWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    def reset(self):
        super().reset()
