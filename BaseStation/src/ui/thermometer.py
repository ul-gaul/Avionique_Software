from PyQt5 import QtWidgets, QtCore, QtGui
from src.ui.utils import set_minimum_expanding_size_policy


class Thermometer(QtWidgets.QWidget):

    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("thermometer_grid_layout")

        self._create_description()
        self._create_temperature_unit()
        self._create_gradient_slider()
        self._create_graduation()
        self._create_spacers()

    def get_layout(self):
        return self.gridLayout

    def set_temperature(self, temperature: float):
        if temperature < 0:
            value = 0
        elif temperature > 100:
            value = 100
        else:
            value = round(temperature)

        self.verticalSlider.setValue(value)

    def _create_description(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setObjectName("thermometer_description_layout")
        left_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        layout.addItem(left_spacer)

        description_label = QtWidgets.QLabel(self.parentWidget())
        description_label.setObjectName("thermometer_description_label")
        description_label.setText("Température")
        layout.addWidget(description_label)

        right_spacer = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        layout.addItem(right_spacer)
        self.gridLayout.addLayout(layout, 0, 0, 1, 1)

    def _create_temperature_unit(self):
        temperature_unit_label = QtWidgets.QLabel(self.parentWidget())
        temperature_unit_label.setObjectName("thermometer_temperature_unit_label")
        temperature_unit_label.setText("°C")
        self.gridLayout.addWidget(temperature_unit_label, 0, 1, 1, 1)

    def _create_graduation(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setObjectName("thermometer_graduation_layout")
        for i in range(11):
            label = self._create_graduation_label(str(100 - 10 * i))
            layout.addWidget(label)
        self.gridLayout.addLayout(layout, 1, 1, 1, 1)

    def _create_gradient_slider(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setObjectName("thermometer_gradient_slider_layout")
        spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        layout.addItem(spacer)
        color_gradient = self._create_color_gradient()
        layout.addWidget(color_gradient)
        vertical_slider = self._create_vertical_slider()
        layout.addWidget(vertical_slider)
        self.gridLayout.addLayout(layout, 1, 0, 1, 1)

    def _create_color_gradient(self):
        color_gradient = QtWidgets.QLabel(self.parentWidget())
        set_minimum_expanding_size_policy(color_gradient)
        color_gradient.setMinimumSize(QtCore.QSize(50, 273))
        color_gradient.setMaximumSize(QtCore.QSize(100, 400))
        color_gradient.setText("")
        color_gradient.setObjectName("thermometer_color_gradient")
        color_gradient.setPixmap(QtGui.QPixmap("resources/gradient.png"))
        return color_gradient

    def _create_vertical_slider(self):
        vertical_slider = QtWidgets.QSlider(self.parentWidget())
        vertical_slider.setEnabled(True)
        vertical_slider.setMaximum(100)
        vertical_slider.setTracking(False)
        vertical_slider.setOrientation(QtCore.Qt.Vertical)
        vertical_slider.setInvertedAppearance(False)
        vertical_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        vertical_slider.setTickInterval(10)
        vertical_slider.setObjectName("thermometer_verticalSlider")
        return vertical_slider

    def _create_graduation_label(self, temperature_graduation: str):
        label = QtWidgets.QLabel(self.parentWidget())
        label.setObjectName("thermometer_label_" + temperature_graduation)
        label.setText(temperature_graduation)
        return label

    def _create_spacers(self):
        top_right_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(top_right_spacer, 0, 2, 1, 1)
        bottom_right_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.MinimumExpanding,
                                                    QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(bottom_right_spacer, 1, 2, 1, 1)
