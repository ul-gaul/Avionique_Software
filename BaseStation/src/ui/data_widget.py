from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pqtg
from src.ui.gl_rocket import GlRocket
from src.ui.header import Header
from src.ui.thermometer import Thermometer
from src.ui.led import Led
from src.ui.utils import *
from src.ui.mainwindow import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pyqtgraph.opengl as gl
import numpy as np


# FIXME: make this class abstract
class DataWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_black_on_white_graph_colors()
        self.thermometer = None
        self.setup_ui()

        self.leds = [self.led_1, self.led_2, self.led_3, self.led_4, self.led_5, self.led_6]
        for i in range(1, 7):
            self.set_led_state(i, False)

        self.graphicsView.plotItem.setTitle("Altitude")
        self.graphicsView.plotItem.setLabel("bottom", "Temps", "Sec")
        self.graphicsView.plotItem.setLabel("left", "Altitude (ft)")
        self.altitude_curve = self.graphicsView.plot([0], [0], pen=pqtg.mkPen(color='k', width=3))
        self.simulation_curve = None

        self.graphicsView_2.plotItem.setTitle("Position relative au camp")
        self.graphicsView_2.plotItem.setLabel("bottom", "Est", "m")
        self.graphicsView_2.plotItem.setLabel("left", "Nord", "m")
        self.graphicsView_2.plotItem.showGrid(x=True, y=True)
        self.positions_on_map = self.graphicsView_2.plot([0], [0], pen=pqtg.mkPen(color='k', width=3))

        """
        cylinder_mesh = gl.MeshData.cylinder(rows=2, cols=10, radius=[1.0, 1.0], length=5.0)
        cone_mesh = gl.MeshData.cylinder(rows=2, cols=10, radius=[1.0, 0.], length=2.0)
        colors = np.zeros((cone_mesh.faceCount(), 4))
        colors[:, :] = [255, 0, 0, 1]
        cone_mesh.setFaceColors(colors)
        self.cylinder_mesh_item = gl.GLMeshItem(meshdata=cylinder_mesh, smooth=False, drawEdges=False,
                                                computeNormals=False)
        self.cone_mesh_item = gl.GLMeshItem(meshdata=cone_mesh, smooth=False, drawEdges=False, computeNormals=False)
        self.cone_mesh_item.setParentItem(self.cylinder_mesh_item)
        self.cone_mesh_item.translate(0, 0, 5)
        self.rocket_vector = gl.GLLinePlotItem(pos=np.array([[0, 0, 0], [3, 0, 0]]), color=[255, 0, 255, 1])
        self.rocket_vector.setParentItem(self.cylinder_mesh_item)
        self.glView.addItem(self.cylinder_mesh_item)
        self.glView.addItem(self.cone_mesh_item)
        self.glView.addItem(self.rocket_vector)
        """

        #self.glRocket.draw_rocket()

    @staticmethod
    def set_black_on_white_graph_colors():
        pqtg.setConfigOption('background', 'w')
        pqtg.setConfigOption('foreground', 'k')

    def setup_ui(self):
        self.setObjectName("Form")
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setObjectName("main_layout")

        self.header = Header(self, 150, 75)
        self.main_layout.addLayout(self.header.get_layout())

        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.setObjectName("horizontal_layout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.graphicsView = pqtg.PlotWidget(self)
        set_minimum_expanding_size_policy(self.graphicsView)
        self.graphicsView.setMinimumSize(QtCore.QSize(400, 150))
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)

        spacerItem2 = QtWidgets.QSpacerItem(20, 70, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)

        self.graphicsView_2 = pqtg.PlotWidget(self)
        set_minimum_expanding_size_policy(self.graphicsView_2)
        self.graphicsView_2.setMinimumSize(QtCore.QSize(400, 150))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.verticalLayout.addWidget(self.graphicsView_2)

        spacerItem3 = QtWidgets.QSpacerItem(20, 70, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontal_layout.addLayout(self.verticalLayout)
        spacerItem4 = QtWidgets.QSpacerItem(90, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontal_layout.addItem(spacerItem4)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        """
        self.glView = gl.GLViewWidget(self)
        set_minimum_expanding_size_policy(self.glView)
        self.glView.setMinimumSize(QtCore.QSize(200, 400))
        self.glView.setCameraPosition(distance=15)
        gx = gl.GLGridItem()
        gx.scale(1, 1, 1)
        self.glView.addItem(gx)
        axis = gl.GLAxisItem(glOptions="additive")
        axis.setSize(5, 5, 5)
        self.glView.addItem(axis)
        self.glView.setObjectName("glView")
        self.verticalLayout_2.addWidget(self.glView)
        """
        """
        self.openGLWidget = QtWidgets.QOpenGLWidget(self)
        set_minimum_expanding_size_policy(self.openGLWidget)
        self.openGLWidget.setMinimumSize(QtCore.QSize(200, 400))
        self.openGLWidget.setObjectName("openGLWidget")
        self.verticalLayout_2.addWidget(self.openGLWidget)
        """
        self.glRocket = GlRocket(self)
        self.verticalLayout_2.addWidget(self.glRocket)

        spacerItem5 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem6 = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem6)
        self.widget = QtWidgets.QWidget(self)
        set_fixed_size_policy(self.widget)
        self.widget.setMinimumSize(QtCore.QSize(280, 73))
        self.widget.setObjectName("widget")
        self.controls_outer_layout = QtWidgets.QHBoxLayout(self.widget)
        self.controls_outer_layout.setContentsMargins(0, 0, 0, 0)
        self.controls_outer_layout.setObjectName("controls_outer_layout")
        self.controls_inner_layout = QtWidgets.QHBoxLayout()
        self.controls_inner_layout.setObjectName("controls_inner_layout")
        self.controls_outer_layout.addLayout(self.controls_inner_layout)
        self.horizontalLayout_4.addWidget(self.widget)
        spacerItem7 = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem7)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontal_layout.addLayout(self.verticalLayout_2)
        spacerItem8 = QtWidgets.QSpacerItem(90, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontal_layout.addItem(spacerItem8)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_4 = QtWidgets.QFrame(self)
        set_minimum_expanding_size_policy(self.frame_4)
        self.frame_4.setMinimumSize(QtCore.QSize(75, 273))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_6.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_6.setSpacing(7)
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        self.led_1 = Led(self, "Acquisition board 1")
        self.verticalLayout_6.addLayout(self.led_1.get_layout())
        self.led_2 = Led(self, "Acquisition board 2")
        self.verticalLayout_6.addLayout(self.led_2.get_layout())
        self.led_3 = Led(self, "Acquisition board 3")
        self.verticalLayout_6.addLayout(self.led_3.get_layout())
        self.led_4 = Led(self, "Power supply 1")
        self.verticalLayout_6.addLayout(self.led_4.get_layout())
        self.led_5 = Led(self, "Power supply 2")
        self.verticalLayout_6.addLayout(self.led_5.get_layout())
        self.led_6 = Led(self, "Payload board")
        self.verticalLayout_6.addLayout(self.led_6.get_layout())

        self.horizontalLayout_3.addWidget(self.frame_4)
        self.thermometer = Thermometer(self)
        self.horizontalLayout_3.addLayout(self.thermometer.get_layout())

        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        spacerItem13 = QtWidgets.QSpacerItem(20, 70, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem13)

        self.graphicsView_3 = pqtg.PlotWidget(self)
        set_minimum_expanding_size_policy(self.graphicsView_3)
        self.graphicsView_3.setMinimumSize(QtCore.QSize(295, 100))
        self.graphicsView_3.setObjectName("graphicsView_3")
        self.verticalLayout_3.addWidget(self.graphicsView_3)

        spacerItem14 = QtWidgets.QSpacerItem(20, 70, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem14)
        self.horizontal_layout.addLayout(self.verticalLayout_3)
        self.main_layout.addLayout(self.horizontal_layout)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("data", "Form"))

    def init_button(self, button, object_name, text, callback):
        set_minimum_expanding_size_policy(button)
        button.setObjectName(object_name)
        button.setText(text)
        button.clicked.connect(callback)
        self.controls_inner_layout.addWidget(button)

    def set_led_state(self, led_num: int, is_on: bool):
        self.leds[led_num - 1].set_state(is_on)

    def set_target_altitude(self, altitude):
        self.graphicsView.plotItem.addLine(y=altitude, pen=pqtg.mkPen(color='r', width=3))

    def draw_altitude(self, values: list):
        self.altitude_curve.setData(values)

    def draw_map(self, eastings: list, northings: list):
        self.positions_on_map.setData(eastings, northings)

    def show_simulation(self, time, altitude):
        if self.simulation_curve is None:
            self.simulation_curve = self.graphicsView.plot(time, altitude, pen=pqtg.mkPen(color='b', width=3))
        else:
            self.simulation_curve.setData(time, altitude)

    def rotate_rocket_model(self, w, x, y, z):
        #tr = pqtg.Transform3D()
        #tr.rotate(w, x, y, z)
        #self.cylinder_mesh_item.setTransform(tr)
        self.glRocket.rotate_rocket(w, x, y, z)

    def set_thermometer_value(self, temperature: float):
        self.thermometer.set_temperature(temperature)
