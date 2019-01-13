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

        self.open_csv_file_action = QAction("Ouvrir un fichier CSV", files_menu)
        self.open_csv_file_action.setObjectName("open_csv_file_action")
        self.open_csv_file_action.setShortcut("Ctrl+O")
        self.open_csv_file_action.setStatusTip("Ouvre le mode replay avec les données de vol sélectionnées")

        self.open_simulation_action = QAction('&Ajouter une simulation', files_menu)
        self.open_simulation_action.setShortcut('Ctrl+A')
        self.open_simulation_action.setStatusTip("Ajoute les données d'une simulation OpenRocket aux graphiques")

        self.edit_preferences = QAction(self)
        self.edit_preferences.setObjectName("edit_preferences")
        self.edit_preferences.setText("Préférences")

        self.exit_action = QAction('&Quitter', files_menu)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setStatusTip("Quitte l'application")

        files_menu.addAction(self.new_acquisition_action)
        files_menu.addAction(self.open_csv_file_action)
        files_menu.addAction(self.open_simulation_action)
        files_menu.addAction(self.edit_preferences)
        files_menu.addSeparator()
        files_menu.addAction(self.exit_action)

        self.addAction(files_menu.menuAction())

    def set_open_simulation_callback(self, callback: Callable):
        self.open_simulation_action.triggered.connect(callback)

    def set_on_exit_callback(self, callback: Callable):
        self.exit_action.triggered.connect(callback)

    def set_edit_preferences_callback(self, callback: Callable):
        self.edit_preferences.triggered.connect(callback)
