from PyQt5.QtWidgets import (
    QFormLayout, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDialog,
    QPushButton, QMessageBox)

from src.ui.config_controller import ConfigController


OTHER_SECTION = "__others__"


class ConfigDialog:
    def __init__(self, parent, *args, **kwargs):
        self.window = QDialog(parent, *args, **kwargs)
        self.window.setModal(True)
        self.window.setWindowTitle("Configuration")
        self.conteneur = QVBoxLayout()
        self.window.setLayout(self.conteneur)
        self.buttons = QHBoxLayout()
        self.buttons.addStretch()
        buttonOk = QPushButton("OK")
        buttonCancel = QPushButton("Annuler")
        buttonOk.clicked.connect(self.save)
        buttonCancel.clicked.connect(self.cancel)
        self.buttons.addWidget(buttonOk)
        self.buttons.addWidget(buttonCancel)
        self.inputs = {}

    def make_ui(self):
        for section_name in self.controller.get_sections():
            header = QLabel(section_name.upper() if not section_name == OTHER_SECTION else "")
            form = QFormLayout()
            for setting in self.controller.get_settings(section_name):
                name = setting["name"]
                value = setting["value"]
                self.inputs[name] = {"section": section_name, "input": QLineEdit(value)}
                form.addRow(QLabel(" ".join(name.split("_")).capitalize()),
                            self.inputs[name]["input"])
            if header.text():
                self.conteneur.addWidget(header)
            self.conteneur.addLayout(form)
            self.conteneur.addSpacing(12)
        self.conteneur.addLayout(self.buttons)
        self.window.exec_()

    def open(self, cheminFichier: str):
        self.controller = ConfigController(cheminFichier)
        self.make_ui()

    def close(self):
        self.window.close()

    def save(self):
        for name, inputItem in self.inputs.items():
            self.controller.set_value(inputItem["section"], name, inputItem["input"].text())
        self.controller.save_to_file()
        QMessageBox.question(self.window, "Configuration", "Settings have been saved !",
                             QMessageBox.Ok, QMessageBox.Ok)

    def cancel(self):
        self.close()
