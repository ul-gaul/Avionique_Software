from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QFileDialog, QWidget, QMenuBar, QMenu, QAction
from PyQt5.QtGui import QIcon, QCloseEvent

from src.ui.homewidget import HomeWidget
from src.ui.real_time_widget import RealTimeWidget
from src.ui.replay_widget import ReplayWidget
from src.real_time_controller import RealTimeController
from src.replay_controller import ReplayController


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = None
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.home_widget = HomeWidget(self)
        self.real_time_widget = None
        self.replay_widget = None
        self.menu_bar = None
        self.files_menu = None
        self.new_acquisition_action = None
        self.open_csv_file_action = None
        self.central_widget.addWidget(self.home_widget)
        self.setWindowIcon(QIcon("src/resources/logo.jpg"))
        self.setWindowTitle("GAUL BaseStation")
        self.set_stylesheet("src/resources/mainwindow.css")

    def add_sim(self):
        filename, _ = QFileDialog.getOpenFileName(caption="Open File", filter="All Files (*);; CSV Files (*.csv)")

        self.controller.add_open_rocket_simulation(filename)
        # TODO: Ajouter le nom de la simulation dans le status bar

    def open_real_time(self):
        self.real_time_widget = RealTimeWidget(self)
        self.controller = RealTimeController(self.real_time_widget)
        self.real_time_widget.set_button_callback(self.controller.real_time_button_callback)
        self.open_new_widget(self.real_time_widget)

    def open_replay(self):
        filename, _ = QFileDialog.getOpenFileName(caption="Open File", filter="All Files (*);; CSV Files (*.csv)")
        self.replay_widget = ReplayWidget(self)
        self.controller = ReplayController(self.replay_widget, filename)
        # TODO: bind replay control buttons to callback in the ReplayController
        self.open_new_widget(self.replay_widget)

    def open_new_widget(self, widget: QWidget):
        self.central_widget.addWidget(widget)
        self.central_widget.setCurrentWidget(widget)
        self.setup_menu_bar()
        self.set_stylesheet("src/resources/data.css")
        self.showMaximized()

    def setup_menu_bar(self):
        self.menu_bar = QMenuBar(self)
        self.statusBar()

        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 1229, 26))
        self.menu_bar.setObjectName("menu_bar")
        self.files_menu = QMenu(self.menu_bar)
        self.files_menu.setObjectName("files_menu")
        self.files_menu.setTitle("Fichiers")
        self.setMenuBar(self.menu_bar)

        exit_act = QAction('&Quitter', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip("Quitte l'application")
        exit_act.triggered.connect(self.close)

        opensim_act = QAction('&Ajouter une simulation', self)
        opensim_act.setShortcut('Ctrl+A')
        opensim_act.setStatusTip("Ajoute les données d'une simulation OpenRocket aux graphiques")
        opensim_act.triggered.connect(self.add_sim)

        self.new_acquisition_action = QAction(self)
        self.new_acquisition_action.setObjectName("new_acquisition_action")
        self.new_acquisition_action.setText("Nouvelle acquisition")

        self.open_csv_file_action = QAction(self)
        self.open_csv_file_action.setObjectName("open_csv_file_action")
        self.open_csv_file_action.setText("Ouvrir un fichier CSV")

        self.files_menu.addAction(self.new_acquisition_action)
        self.files_menu.addAction(self.open_csv_file_action)
        self.files_menu.addAction(opensim_act)
        self.files_menu.addAction(exit_act)
        self.menu_bar.addAction(self.files_menu.menuAction())

    def set_stylesheet(self, stylesheet_path):
        file = open(stylesheet_path, 'r')
        stylesheet = file.read()
        self.setStyleSheet(stylesheet)

    def closeEvent(self, event: QCloseEvent):
        if self.controller is not None:
            self.controller.on_close(event)
        else:
            event.accept()
