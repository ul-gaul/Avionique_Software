import sys
import pyqtgraph as pg
import numpy as np
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtCore import QCoreApplication

app = QApplication(sys.argv)

x = np.random.normal(loc=0.0, scale=2, size=100)

widget = pg.PlotWidget(title="Some Plotting")
widget.setWindowTitle("Random Plotting")
widget.plotItem.plot(x)
widget.show()

sys.exit(app.exec_())