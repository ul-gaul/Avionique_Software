from src.ui.data_widget import DataWidget
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy


class ReplayWidget(DataWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.horizontalLayout_5 = None
        self.rewind_button = None
        self.play_pause_button = None
        self.fast_forward_button = None
        self.init_all_buttons()

    def init_all_buttons(self):
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.init_button(self.rewind_button, "rewind_button", "RW", self.rewind)
        self.init_button(self.play_pause_button, "play_pause_button", "Play", self.play)
        self.init_button(self.fast_forward_button, "fast_forward_button", "FF", self.fast_forward)
        
        self.horizontalLayout.addLayout(self.horizontalLayout_5)

    def init_button(self, button, object_name, text, callback):
        button = QPushButton(self.widget)
        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
        button.setSizePolicy(size_policy)
        button.setObjectName(object_name)
        button.setText(text)
        button.clicked.connect(callback)
        self.horizontalLayout_5.addWidget(button)

    def rewind(self):
        print("rewind")

    def play(self):
        print("play")

    def pause(self):
        print("pause")

    def fast_forward(self):
        print("fast forward")
