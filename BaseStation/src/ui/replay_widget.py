from PyQt5.QtWidgets import QPushButton, QLabel
from src.ui.data_widget import DataWidget
from src.ui.ExtendedQSlider import ExtendedQSlider


class ReplayWidget(DataWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.horizontalSlider = ExtendedQSlider(self, "horizontalSlider")
        self.main_layout.addWidget(self.horizontalSlider)
        self.callbacks = {}
        self.rewind_button = QPushButton(self.widget)
        self.init_button(self.rewind_button, "rewind_button", "RW", self.rewind)
        self.play_pause_button = QPushButton(self.widget)
        self.init_button(self.play_pause_button, "play_pause_button", "Play", self.play)
        self.fast_forward_button = QPushButton(self.widget)
        self.init_button(self.fast_forward_button, "fast_forward_button", "FF", self.fast_forward)
        self.speedLabel = QLabel()
        self.main_layout.addWidget(self.speedLabel)

    def set_callback(self, name, func):
        self.callbacks.update({name: func})

    def rewind(self):
        print("rewind")
        try:
            self.callbacks["rewind"]()
        except KeyError:
            pass

    def play(self):
        print("play")
        self.play_pause_button.setText('Pause')
        self.play_pause_button.clicked.disconnect(self.play)
        self.play_pause_button.clicked.connect(self.pause)
        try:
            self.callbacks["play"]()
        except KeyError:
            pass

    def pause(self):
        print("pause")
        self.play_pause_button.setText('Play')
        self.play_pause_button.clicked.disconnect(self.pause)
        self.play_pause_button.clicked.connect(self.play)
        try:
            self.callbacks["pause"]()
        except KeyError:
            pass

    def fast_forward(self):
        print("fast forward")
        try:
            self.callbacks["fast_forward"]()
        except KeyError:
            pass

    def update_replay_speed_text(self, speed):
        self.speedLabel.setText('{}x'.format(speed))
