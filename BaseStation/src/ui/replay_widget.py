from PyQt5.QtWidgets import QPushButton
from src.ui.data_widget import DataWidget
from src.ui.ExtendedQSlider import ExtendedQSlider


class ReplayWidget(DataWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.horizontalSlider = ExtendedQSlider(self, "horizontalSlider")
        self.main_layout.addWidget(self.horizontalSlider)
        self.rewind_button = QPushButton(self.widget)
        self.init_button(self.rewind_button, "rewind_button", "RW", self.rewind)
        self.play_pause_button = QPushButton(self.widget)
        self.init_button(self.play_pause_button, "play_pause_button", "Play", self.play)
        self.fast_forward_button = QPushButton(self.widget)
        self.init_button(self.fast_forward_button, "fast_forward_button", "FF", self.fast_forward)

    def rewind(self):
        print("rewind")

    def play(self):
        print("play")

    def pause(self):
        print("pause")

    def fast_forward(self):
        print("fast forward")
