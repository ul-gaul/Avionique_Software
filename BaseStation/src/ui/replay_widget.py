from PyQt5.QtWidgets import QPushButton, QLabel
from src.ui.data_widget import DataWidget
from src.ui.control_bar import ControlBar


class ReplayWidget(DataWidget):

    PLAY_TEXT = "Play"
    PAUSE_TEXT = "Pause"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.control_bar = ControlBar(self, "control_bar")
        self.main_layout.addWidget(self.control_bar)
        self.callbacks = {}
        self.rewind_button = QPushButton(self.widget)
        self.init_button(self.rewind_button, "rewind_button", "RW", self.rewind)
        self.play_pause_button = QPushButton(self.widget)
        self.init_button(self.play_pause_button, "play_pause_button", self.PLAY_TEXT, self.play)
        self.fast_forward_button = QPushButton(self.widget)
        self.init_button(self.fast_forward_button, "fast_forward_button", "FF", self.fast_forward)
        self.speedLabel = QLabel()
        self.main_layout.addWidget(self.speedLabel)

    def set_callback(self, name, func):
        self.callbacks.update({name: func})

    def rewind(self):
        try:
            self.callbacks["rewind"]()
        except KeyError:
            pass

    def play(self):
        self.play_pause_button.setText(self.PAUSE_TEXT)
        self.play_pause_button.clicked.disconnect(self.play)
        self.play_pause_button.clicked.connect(self.pause)
        try:
            self.callbacks["play"]()
        except KeyError:
            pass

    def pause(self):
        self.play_pause_button.setText(self.PLAY_TEXT)
        self.play_pause_button.clicked.disconnect(self.pause)
        self.play_pause_button.clicked.connect(self.play)
        try:
            self.callbacks["pause"]()
        except KeyError:
            pass

    def fast_forward(self):
        try:
            self.callbacks["fast_forward"]()
        except KeyError:
            pass

    def update_play_pause_button_text(self, is_paused: bool):   #TODO
        if is_paused:
            self.play_pause_button.setText(self.PLAY_TEXT)
        else:
            self.play_pause_button.setText(self.PAUSE_TEXT)

    def update_replay_speed_text(self, speed):
        self.speedLabel.setText('{}x'.format(speed))

    def set_control_bar_max_value(self, max_value: int):
        self.control_bar.setMaximum(max_value)

    def set_control_bar_current_value(self, value: int):
        self.control_bar.setValue(value)

    def set_control_bar_callback(self, callback):
        self.control_bar.set_callback(callback)

    def reset(self):
        super().reset()
        self.set_control_bar_max_value(1)
        self.set_control_bar_current_value(0)
        self.update_replay_speed_text(1)
