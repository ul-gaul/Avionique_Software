from PyQt5.QtWidgets import QLCDNumber, QPushButton, QMessageBox, QFileDialog

from src.ui.data_main_window import DataMainWindow
from src.ui.utils import set_minimum_expanding_size_policy


class RealTimeWidget(DataMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_stop_button_callback = lambda: False
        self.start_stop_button = QPushButton(self.widget)
        self.init_button(self.start_stop_button, "start_stop_button", "Démarrer l'acquisition", self.on_button_click)

        self.lcdNumber = QLCDNumber(self.widget)
        set_minimum_expanding_size_policy(self.lcdNumber)
        self.lcdNumber.setObjectName("lcdNumber")
        self.controls_inner_layout.addWidget(self.lcdNumber)

    def set_button_callback(self, start_stop_button_callback):
        self.start_stop_button_callback = start_stop_button_callback

    def on_button_click(self):
        self.start_stop_button_callback()

    def update_button_text(self, is_acquisition_running: bool):
        if is_acquisition_running:
            self.start_stop_button.setText("Arrêter l'acquisition")
        else:
            self.start_stop_button.setText("Démarrer l'acquisition")

    def set_time(self, time):
        self.lcdNumber.display(time)

    def reset(self):
        super().reset()
        self.set_time(0)

    def show_save_message_box(self) -> QMessageBox.StandardButton:
        message_box = QMessageBox()
        return message_box.question(self, "BaseStation",
                                    "Vous avez des données non sauvegardées.\nVoulez-vous les sauvegarder?",
                                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)

    @staticmethod
    def get_save_file_name(default_path: str) -> str:
        filename, _ = QFileDialog.getSaveFileName(caption="Save File", directory=default_path,
                                                  filter="All Files (*);; CSV Files (*.csv)",
                                                  options=QFileDialog.Options())
        return filename
