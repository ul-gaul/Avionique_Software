import os
from PyQt5.QtWidgets import (
    QFormLayout, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDialog,
    QPushButton, QMessageBox, QListWidget)
from PyQt5 import QtGui

from src.ui.config_controller import ConfigController


OTHER_SECTION = "__others__"


class ConfigDialog:
    def __init__(self, parent, *args, **kwargs):
        self._make_window()
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

    def _make_window(self, parent=None):
        self.window = QDialog(parent)
        self.window.setModal(True)
        self.window.setWindowTitle("Configuration")
        self.conteneur = QVBoxLayout()
        self.window.setLayout(self.conteneur)

    def _make_ui(self):
        self._clear_ui()
        self._set_stylesheet()
        self._set_layouts()
        self._show_waiting_msg()
        self.window.show()
        QtGui.QGuiApplication.processEvents()
        headers = []
        layouts = []
        spacings = []

        for section_name in self.controller.get_sections():
            header = QLabel(section_name.upper()) if not section_name == OTHER_SECTION else None
            form = QFormLayout()
            for name, (value, input_type, label) in self.controller.get_settings(section_name):
                if input_type.endswith('list'):
                    input_el = QListWidget()
                    input_el.addItems(value)
                else:
                    input_el = QLineEdit(value)
                self.inputs[name] = {
                    "section": section_name,
                    "input": input_el,
                    "type": input_type}
                label_ = label or " ".join(name.split("_"))
                form.addRow(QLabel(label_[0].capitalize() + "".join(label_[1:])),
                            self.inputs[name]["input"])
            if header is not None:
                header.setProperty("SectionHeader", True)
            headers.append(header)
            layouts.append(form)
            spacings.append(12)

        self.window.hide()
        self._hide_waiting_msg()

        for header, layout, spacing in zip(headers, layouts, spacings):
            if header is not None:
                self.conteneur.addWidget(header)
            self.conteneur.addLayout(layout)
            self.conteneur.addSpacing(spacing)
        self.conteneur.addLayout(self.buttons)
        self.window.exec_()

    def _show_waiting_msg(self):
        layout = QVBoxLayout()
        msg = QLabel("Chargement des paramètres...")
        layout.addWidget(msg)
        self.conteneur.addLayout(layout)

    def _hide_waiting_msg(self):
        self._clear_ui()

    def open(self, cheminFichier: str):
        self.controller = ConfigController(cheminFichier)
        self._make_window()
        self._clear_inputs()
        self._make_ui()

    def close(self):
        self.window.close()

    def save(self):
        for name, inputItem in self.inputs.items():
            self.controller.set_value(
                inputItem["section"], name, self._get_value(inputItem["input"], inputItem["type"]))
        self.controller.save_to_file()
        QMessageBox.question(self.window, "Configuration", "Settings have been saved !",
                             QMessageBox.Ok, QMessageBox.Ok)
        self.close()

    @staticmethod
    def _get_value(input_el, input_type):
        if input_type.endswith('list'):
            return input_el.currentItem().text()
        return input_el.text()

    def cancel(self):
        self.close()
