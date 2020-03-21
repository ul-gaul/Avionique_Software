from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout


class TabsWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.widgets_in_tabs = []

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.resize(300, 200)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def clearTabs(self):
        self.widgets_in_tabs.clear()
        self.tabs.clear()

    def addWidget(self, widget: QWidget, tab_name: str):
        self.widgets_in_tabs.append(widget)
        self.tabs.addTab(self.widgets_in_tabs[-1], tab_name)

