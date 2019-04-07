from typing import Callable
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QAction, QMenu, QMenuBar, QWidget


class MenuBar(QMenuBar):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setGeometry(QRect(0, 0, 1229, 26))
        self.setObjectName("menu_bar")

        files_menu = QMenu(self)
        files_menu.setObjectName("files_menu")
        files_menu.setTitle("Fichiers")

        self.new_acquisition_action = QAction("Nouvelle acquisition", files_menu)
        self.new_acquisition_action.setObjectName("new_acquisition_action")
        self.new_acquisition_action.setShortcut("Ctrl+N")
        self.new_acquisition_action.setStatusTip("Démarre une nouvelle acquisition des données de vol")

        self.save_as_action = QAction("Enregistrer sous", files_menu)
        self.save_as_action.setObjectName("save_as_action")
        self.save_as_action.setShortcut("Ctrl+S")
        self.save_as_action.setStatusTip("Enregistrer les données de vol dans un fichier CSV")
        self.save_as_action.setEnabled(False)

        self.load_flight_data_action = QAction("Charger des données de vol", files_menu)
        self.load_flight_data_action.setObjectName("load_flight_data_action")
        self.load_flight_data_action.setShortcut("Ctrl+O")
        self.load_flight_data_action.setStatusTip("Ouvre le mode replay avec les données de vol sélectionnées")

        self.open_simulation_action = QAction('&Ajouter une simulation', files_menu)
        self.open_simulation_action.setObjectName("open_simulation_action")
        self.open_simulation_action.setShortcut('Ctrl+A')
        self.open_simulation_action.setStatusTip("Ajoute les données d'une simulation OpenRocket aux graphiques")
        self.open_simulation_action.setEnabled(False)

        self.console_action = QAction('Console', files_menu)
        self.console_action.setShortcut('Ctrl+C')
        self.console_action.setStatusTip("Console de deboggage")

        self.edit_preferences_action = QAction("Préférences", files_menu)
        self.edit_preferences_action.setObjectName("edit_preferences_action")
        self.edit_preferences_action.setStatusTip("Ouvre la fenêtre des paramètres de l'application")

        self.exit_action = QAction('&Quitter', files_menu)
        self.edit_preferences_action.setObjectName("exit_action")
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setStatusTip("Quitte l'application")

        files_menu.addAction(self.new_acquisition_action)
        files_menu.addAction(self.save_as_action)
        files_menu.addAction(self.load_flight_data_action)
        files_menu.addAction(self.open_simulation_action)

        files_menu.addAction(self.console_action)

        files_menu.addAction(self.edit_preferences_action)
        files_menu.addSeparator()
        files_menu.addAction(self.exit_action)

        self.addAction(files_menu.menuAction())

    def set_new_acquisition_callback(self, callback: Callable[[], None]):
        self.new_acquisition_action.triggered.connect(callback)

    def set_save_as_callback(self, callback: Callable[[], None]):
        self.save_as_action.triggered.connect(callback)

    def set_load_flight_data_callback(self, callback: Callable[[], None]):
        self.load_flight_data_action.triggered.connect(callback)

    def set_open_simulation_callback(self, callback: Callable[[], None]):
        self.open_simulation_action.triggered.connect(callback)

    def set_on_exit_callback(self, callback: Callable[[], None]):
        self.exit_action.triggered.connect(callback)

    def set_edit_preferences_callback(self, callback: Callable):
        self.edit_preferences_action.triggered.connect(callback)

    def set_console_callback(self, callback: Callable):
        self.console_action.triggered.connect(callback)

    def set_real_time_mode(self):
        self.save_as_action.setEnabled(True)
        self.open_simulation_action.setEnabled(True)

    def set_replay_mode(self):
        self.save_as_action.setEnabled(False)
        self.open_simulation_action.setEnabled(True)
