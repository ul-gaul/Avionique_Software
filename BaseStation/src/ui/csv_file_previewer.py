import sys
from PyQt5.QtWidgets import (QApplication, QWidget,  QSizePolicy, QSpacerItem, QVBoxLayout, QPushButton, QHBoxLayout,
                             QTextBrowser)


class CsvFilePreviewer(QWidget):

    def __init__(self, header, data, parent=None):
        super().__init__(parent=parent)
        self.header = header
        self.data = data
        self.textBrowser = None
        self.initUI()
        self.write(self.header)
        # self.write(self.data)

    def init_ui(self):
        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout()
        self.textBrowser = QTextBrowser(self)
        self.textBrowser.setFontPointSize(7)
        save_btn = QPushButton("Save", self)
        # save_btn.clicked.connect(self.saveCSV)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        vbox.addItem(spacerItem)
        vbox.addWidget(self.textBrowser)
        spacerItem1 = QSpacerItem(10, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        hbox.addItem(spacerItem1)
        hbox.addWidget(save_btn)
        vbox.addLayout(hbox)

        self.setGeometry(300, 300, 1085, 250)
        self.setWindowTitle("Rocket Packet Preview")

    def write(self, data):
        self.textBrowser.insertPlainText((", ".join(data)))

"""For testing purpose"""
if __name__ == '__main__':
    HEADER_FIELDS = ["TIME STAMP",
                     "ANG SPEED X",
                     "ANG SPEED Y",
                     "ANG SPEED Z",
                     "ACCEL X",
                     "ACCEL Y",
                     "ACCEL Z",
                     "MAGNET X",
                     "MAGNET Y",
                     "MAGNET Z",
                     "ALTITUDE",
                     "LATITUDE 1",
                     "LONGITUDE 1",
                     "LATITUDE 2",
                     "LONGITUDE 2",
                     "TEMPERATURE 1",
                     "TEMPERATURE 2"]
    app = QApplication(sys.argv)
    f = CsvFilePreviewer(HEADER_FIELDS, None)
    f.show()
    sys.exit(app.exec_())
