from PyQt5.QtGui import QIcon, QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QFileDialog, QWidget

from src.controller_factory import ControllerFactory
from src.ui.homewidget import HomeWidget
from src.ui.menu_bar import MenuBar
from src.ui.real_time_widget import RealTimeWidget
from src.ui.replay_widget import ReplayWidget
from src.ui.status_bar import StatusBar


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller_factory = ControllerFactory()
        self.controller = None
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)

        self.home_widget = HomeWidget(self)
        self.real_time_widget = None
        self.replay_widget = None
        self.menu_bar = None
        self.central_widget.addWidget(self.home_widget)
        self.setWindowIcon(QIcon("src/resources/logo.jpg"))
        self.setWindowTitle("GAUL BaseStation")
        self.set_stylesheet("src/resources/mainwindow.css")

    def add_simulation(self):
        filename, _ = QFileDialog.getOpenFileName(caption="Open File", directory="./src/resources/",
                                                  filter="All Files (*);; CSV Files (*.csv)")
        if filename != "":
            self.controller.add_open_rocket_simulation(filename)

    def open_real_time(self):
        self.real_time_widget = RealTimeWidget(self)
        self.controller = self.controller_factory.create_real_time_controller(self.real_time_widget)
        self.controller.register_message_listener(self.status_bar)
        self.open_new_widget(self.real_time_widget)

    def open_replay(self):
        filename, _ = QFileDialog.getOpenFileName(caption="Open File", directory="./src/resources/",
                                                  filter="All Files (*);; CSV Files (*.csv)")
        if filename != "":
            self.replay_widget = ReplayWidget(self)
            self.controller = self.controller_factory.create_replay_controller(self.replay_widget, filename)
            self.controller.register_message_listener(self.status_bar)
            self.open_new_widget(self.replay_widget)

    def open_new_widget(self, widget: QWidget):
        self.central_widget.addWidget(widget)
        self.central_widget.setCurrentWidget(widget)
        self.setup_menu_bar()
        self.set_stylesheet("src/resources/data_widget.css")
        self.showMaximized()

    def setup_menu_bar(self):
        self.menu_bar = MenuBar(self)
        self.menu_bar.set_open_simulation_callback(self.add_simulation)
        self.menu_bar.set_on_exit_callback(self.close)
        self.setMenuBar(self.menu_bar)

    def set_stylesheet(self, stylesheet_path):
        file = open(stylesheet_path, 'r')
        stylesheet = file.read()
        self.setStyleSheet(stylesheet)

    def closeEvent(self, event: QCloseEvent):
        if self.controller is not None:
            self.controller.on_close(event)
        else:
            event.accept()
