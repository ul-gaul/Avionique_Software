import os
from PyQt5.QtWidgets import (
    QFormLayout, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDialog,
    QPushButton, QMessageBox, QListWidget, QListWidgetItem)

from src.ui.config_controller import ConfigController


OTHER_SECTION = "__others__"


class ConfigDialog:
    def __init__(self, parent, *args, **kwargs):
        self.window = QDialog(parent, *args, **kwargs)
        self.window.setModal(True)
        self.window.setWindowTitle("Configuration")
        self.conteneur = QVBoxLayout()
        self.window.setLayout(self.conteneur)
        self.set_stylesheet(os.path.join(os.getcwd(), "src/resources/configdialog.css"))

    def set_stylesheet(self, stylesheet_path):
        file = open(stylesheet_path, "r")
        self.stylesheet = file.read()

    def _set_stylesheet(self):
        self.window.setStyleSheet(self.stylesheet)

    def _clear_inputs(self):
        self.inputs = {}

    def _clear_ui(self):
        while self.conteneur.count():
            child = self.conteneur.takeAt(0)
            try:
                self.conteneur.removeWidget(child.widget())
            except TypeError:
                self.conteneur.removeItem(child)
            if child.widget():
                child.widget().setParent(None)

    def _set_layouts(self):
        self.buttons = QHBoxLayout()
        self.buttons.addStretch()
        buttonOk = QPushButton("OK")
        buttonCancel = QPushButton("Annuler")
        buttonOk.setObjectName("btnOk")
        buttonCancel.setObjectName("btnCancel")
        buttonOk.clicked.connect(self.save)
        buttonCancel.clicked.connect(self.cancel)
        self.buttons.addWidget(buttonOk)
        self.buttons.addWidget(buttonCancel)

    def _make_ui(self):
        self._clear_ui()
        self._set_stylesheet()
        self._set_layouts()
        for idx, section_name in enumerate(self.controller.get_sections()):
            header = QLabel(section_name.upper()) if not section_name == OTHER_SECTION else None
            form = QFormLayout()
            for name, (value, input_type) in self.controller.get_settings(section_name):
                if input_type.endswith('list'):
                    input_el = QListWidget()
                    input_el.addItems(value)
                else:
                    input_el = QLineEdit(value)
                self.inputs[name] = {"section": section_name, "input": input_el}
                label = " ".join(name.split("_"))
                form.addRow(QLabel(label[0].capitalize() + "".join(label[1:])),
                            self.inputs[name]["input"])
            if header is not None:
                header.setProperty("SectionHeader", True)
                self.conteneur.addWidget(header)
            self.conteneur.addLayout(form)
            self.conteneur.addSpacing(12)
        self.conteneur.addLayout(self.buttons)
        self.window.exec_()

    def open(self, cheminFichier: str):
        self.controller = ConfigController(cheminFichier)
        self._clear_inputs()
        self._make_ui()

    def close(self):
        self.window.close()

    def save(self):
        for name, inputItem in self.inputs.items():
            self.controller.set_value(inputItem["section"], name, inputItem["input"].text())
        self.controller.save_to_file()
        QMessageBox.question(self.window, "Configuration", "Settings have been saved !",
                             QMessageBox.Ok, QMessageBox.Ok)
        self.close()

    def cancel(self):
        self.close()
