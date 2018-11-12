from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt
from typing import Callable


class ControlBar(QSlider):

    def __init__(self, parent, object_name: str):
        super().__init__(parent)
        self.setEnabled(True)
        self.setRange(0, 100)
        self.setPageStep(1)
        self.setTracking(False)
        self.setMouseTracking(False)
        self.setOrientation(Qt.Horizontal)
        self.setTickPosition(QSlider.NoTicks)
        self.setObjectName(object_name)
        self.callback = lambda index: None

    def set_callback(self, new_callback: Callable[[int], None]):
        self.callback = new_callback

    def compute_position(self, q_mouse_event: QMouseEvent):
        value_range = self.maximum() - self.minimum()

        if self.orientation() == Qt.Vertical:
            new_value = round(self.minimum() + (value_range * (self.height() - q_mouse_event.y())) / self.height())
        else:
            new_value = round(self.minimum() + (value_range * q_mouse_event.x()) / self.width())

        if self.invertedAppearance():
            self.setValue(self.maximum() - new_value)
        else:
            self.setValue(new_value)

    def mousePressEvent(self, q_mouse_event: QMouseEvent):
        if q_mouse_event.button() == Qt.LeftButton:
            self._handle_mouse_event(q_mouse_event)

    def mouseMoveEvent(self, q_mouse_event: QMouseEvent):
        self._handle_mouse_event(q_mouse_event)
        super().mouseMoveEvent(q_mouse_event)

    def _handle_mouse_event(self, q_mouse_event: QMouseEvent):
        self.compute_position(q_mouse_event)
        self.callback(self.value())
        q_mouse_event.accept()
