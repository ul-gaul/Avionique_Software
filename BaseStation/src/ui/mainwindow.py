from datetime import datetime as d
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from src.ui.homewidget import HomeWidget
from src.ui.real_time_widget import RealTimeWidget


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.central_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.home_widget = HomeWidget(self)
        self.real_time_widget = None
        self.replay_widget = None
        self.menuBar = None
        self.menuFichiers = None
        self.actionNouvelle_acquisition = None
        self.actionOuvrir_un_fichier_CSV = None
        self.central_widget.addWidget(self.home_widget)
        self.setWindowIcon(QIcon("resources/logo.jpg"))
        self.set_stylesheet("resources/mainwindow.css")

    def open_real_time(self):
        """  """
        print("real time")
        filename = QtWidgets.QFileDialog.getSaveFileName(caption="Save File",
                                                         directory=d.now().strftime("%Y-%m-%d_%Hh%Mm")+".csv",
                                                         filter="All Files (*);; CSV Files (*.csv)")
        self.real_time_widget = RealTimeWidget(self)
        self.central_widget.addWidget(self.real_time_widget)
        self.central_widget.setCurrentWidget(self.real_time_widget)
        self.setup_menu_bar()
        self.set_stylesheet("resources/data.css")
        #real_time_dialog = DataRT(self.main_window)

    def open_replay(self):
        """   """
        print("replay")
        filename = QtWidgets.QFileDialog.getSaveFileName(caption="Save File",
                                                         directory=d.now().strftime("%Y-%m-%d_%Hh%Mm")+".csv",
                                                         filter="All Files (*);; CSV Files (*.csv)")
        #replay_dialog = Data(self.main_window)
        #replay_dialog.openFileName()

    def setup_menu_bar(self):
        self.menuBar = QtWidgets.QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1229, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuFichiers = QtWidgets.QMenu(self.menuBar)
        self.menuFichiers.setObjectName("menuFichiers")
        self.menuFichiers.setTitle("Fichiers")
        self.setMenuBar(self.menuBar)

        self.actionNouvelle_acquisition = QtWidgets.QAction(self)
        self.actionNouvelle_acquisition.setObjectName("actionNouvelle_acquisition")
        self.actionNouvelle_acquisition.setText("Nouvelle acquisition")

        self.actionOuvrir_un_fichier_CSV = QtWidgets.QAction(self)
        self.actionOuvrir_un_fichier_CSV.setObjectName("actionOuvrir_un_fichier_CSV")
        self.actionOuvrir_un_fichier_CSV.setText("Ouvrir un fichier CSV")

        self.menuFichiers.addAction(self.actionNouvelle_acquisition)
        self.menuFichiers.addAction(self.actionOuvrir_un_fichier_CSV)
        self.menuBar.addAction(self.menuFichiers.menuAction())

    def set_stylesheet(self, stylesheet_path):
        f = open(stylesheet_path, 'r')
        stylesheet = f.read()
        self.setStyleSheet(stylesheet)
