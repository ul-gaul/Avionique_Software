import sys
import ctypes
from PyQt5 import QtWidgets
from BaseStation.src.ui.mainwindow import MainWindow

# FIXME: CLEAN UP ALL THIS SHIT ...
myappid = 'C:\\Users\Lord\Anaconda3\python.exe'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook
# FIXME: ... UP TO HERE !!!!!!!

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
