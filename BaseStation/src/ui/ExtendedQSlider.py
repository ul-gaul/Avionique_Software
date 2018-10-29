from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt


class ExtendedQSlider(QSlider):

    def __init__(self, parent, object_name: str):
        super().__init__(parent)
        self.setEnabled(True)
        self.setRange(0, 100)
        self.setPageStep(1)
        self.setSliderPosition(0)
        self.setTracking(True)
        self.setOrientation(Qt.Horizontal)
        self.setTickPosition(QSlider.NoTicks)
        self.setObjectName(object_name)

    def mousePressEvent(self, q_mouse_event):
        if q_mouse_event.button() == Qt.LeftButton:
            value_range = self.maximum() - self.minimum()
            if self.orientation() == Qt.Vertical:
                new_value = self.minimum() + (value_range * (self.height() - q_mouse_event.y())) / self.height()
            else:
                new_value = q_mouse_event.x() / self.width() * 100

            if self.invertedAppearance():
                self.setValue(self.maximum() - new_value)
            else:
                self.setValue(round(new_value))

            q_mouse_event.accept()

        super().mousePressEvent(q_mouse_event)