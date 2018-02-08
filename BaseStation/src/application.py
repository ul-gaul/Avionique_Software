import sys
import ctypes
from PyQt5 import QtWidgets
from ui.mainwindow import MainWindow


class Application:

    def __init__(self):
        if sys.platform.startswith('win'):
            Application.set_app_user_model_id()

        Application.override_exception_hook()

        self.app = QtWidgets.QApplication(sys.argv)
        self.window = MainWindow()
        self.window.show()
        sys.exit(self.app.exec_())

    @staticmethod
    def set_app_user_model_id():
        app_user_model_id = "ca.ulaval.gaul.basestation"  # must be a unicode string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_user_model_id)

    @staticmethod
    def override_exception_hook():
        """
        Back up the reference to the exception hook and set the exception hook to our wrapping function.
        This is required to prevent Qt from crashing without printing the stacktrace.
        """
        initial_exception_hook = sys.excepthook

        def exception_hook_wrapper(exception_type, value, traceback):
            # Print the error and traceback
            print(exception_type, value, traceback)
            # Call the normal Exception hook after
            initial_exception_hook(exception_type, value, traceback)
            sys.exit(1)

        sys.excepthook = exception_hook_wrapper
