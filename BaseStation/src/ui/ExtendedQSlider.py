from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt


class ExtendedQSlider(QSlider):

    def __init__(self, parent):
        super().__init__(parent)

    def mousePressEvent(self, q_mouse_event):
        if q_mouse_event.button() == Qt.LeftButton:
            value_range = self.maximum() - self.minimum()
            if self.orientation() == Qt.Vertical:
                new_value = self.minimum() + (value_range * (self.height() - q_mouse_event.y())) / self.height()
            else:
                new_value = self.minimum() + (value_range * q_mouse_event.x()) / self.width()

            if self.invertedAppearance():
                self.setValue(self.maximum() - new_value)
            else:
                self.setValue(new_value)
            q_mouse_event.accept()

        super().mousePressEvent(q_mouse_event)
