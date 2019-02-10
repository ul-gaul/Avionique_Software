import os

from PyQt5.QtGui import QIcon, QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QFileDialog, QWidget

from src.controller_factory import ControllerFactory
from src.message_type import MessageType
from src.realtime.rocket_packet_parser_factory import RocketPacketVersionException
from src.ui.console_message_listener import ConsoleMessageListener
from src.ui.homewidget import HomeWidget
from src.ui.menu_bar import MenuBar
from src.ui.real_time_widget import RealTimeWidget
from src.ui.replay_widget import ReplayWidget
from src.ui.status_bar import StatusBar
from src.ui.configdialog import ConfigDialog


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
        self.menu_bar = self.create_menu_bar()
        self.config_dialog = None
        self.central_widget.addWidget(self.home_widget)
        self.setWindowIcon(QIcon("src/resources/logo.jpg"))
        self.setWindowTitle("GAUL BaseStation")
        self.set_stylesheet("src/resources/mainwindow.css")
        self.console = ConsoleMessageListener()

    def create_menu_bar(self):
        menu_bar = MenuBar(self)

        menu_bar.set_save_as_callback(self.save_as)
        menu_bar.set_open_simulation_callback(self.add_simulation)
        menu_bar.set_edit_preferences_callback(self.open_preferences)
        menu_bar.set_on_exit_callback(self.close)

        self.setMenuBar(menu_bar)

        return menu_bar

    def save_as(self):
        pass

    def add_simulation(self):
        filename, _ = QFileDialog.getOpenFileName(caption="Open File", directory="./src/resources/",
                                                  filter="All Files (*);; CSV Files (*.csv)")
        if filename:
            self.controller.add_open_rocket_simulation(filename)

    def open_preferences(self):
        config_path = os.path.join(os.getcwd(), "config.ini")
        if self.config_dialog is None:
            self.config_dialog = ConfigDialog(self)
        self.config_dialog.open(config_path)

    def open_real_time(self):
        try:
            self.real_time_widget = RealTimeWidget(self)
            self.controller = self.controller_factory.create_real_time_controller(self.real_time_widget, self.console)
            self.controller.register_message_listener(self.status_bar)
            self.open_new_widget(self.real_time_widget)
            self.menu_bar.set_real_time_mode()
        except RocketPacketVersionException as error:
            self.real_time_widget = None
            self.status_bar.notify(str(error), MessageType.ERROR)

    def open_replay(self):
        filename, _ = QFileDialog.getOpenFileName(caption="Open File", directory="./src/resources/",
                                                  filter="All Files (*);; CSV Files (*.csv)")
        if filename:
            self.replay_widget = ReplayWidget(self)
            self.controller = self.controller_factory.create_replay_controller(self.replay_widget, filename)
            self.controller.register_message_listener(self.status_bar)
            self.open_new_widget(self.replay_widget)
            self.menu_bar.set_replay_mode()

    def open_new_widget(self, widget: QWidget):
        self.central_widget.addWidget(widget)
        self.central_widget.setCurrentWidget(widget)
        self.set_stylesheet("src/resources/data_widget.css")
        self.showMaximized()
        self.status_bar.clear()

    def set_stylesheet(self, stylesheet_path):
        file = open(stylesheet_path, 'r')
        stylesheet = file.read()
        self.setStyleSheet(stylesheet)

    def closeEvent(self, event: QCloseEvent):
        if self.controller is not None:
            self.controller.on_close(event)
        else:
            event.accept()
