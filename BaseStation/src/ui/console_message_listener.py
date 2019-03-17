from src.message_listener import MessageListener
from src.message_type import MessageType
from src.ui.utils import read_stylesheet

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, QVBoxLayout, QPushButton, QShortcut, QScrollArea, QGroupBox, QGridLayout, QDockWidget
from PyQt5.QtGui import QPixmap, QPainter, QColor, QKeySequence

# Tout mettre dans une array => Les bouttons
# Lambda fonctions.

class MessageConsoleContainer(QWidget):

    def __init__(self, m_type: MessageType, message: str, parent):
        super().__init__(parent)

        self.active = True
        self.message_type = m_type
        self.message = message

        self.groupBox = QGroupBox(m_type.name)

        self.img_lb = QLabel(self)

        text_lb = QTextEdit(self)
        text_lb.setPlainText(self.message)
        text_lb.setReadOnly(True)
        text_lb.setFixedHeight(50)

        self.determine_img()

        vbox = QVBoxLayout()
        vbox.addWidget(self.img_lb)
        vbox.addWidget(text_lb)
        vbox.addStretch(1)
        vbox.addSpacing(1)
        self.groupBox.setLayout(vbox)

    def determine_img(self):
        if self.message_type == MessageType.INFO:
            self.img_lb.setPixmap(QPixmap('src/resources/console_info.png'))
        elif self.message_type == MessageType.DEBUG:
            self.img_lb.setPixmap(QPixmap('src/resources/console_debug.png'))
        elif self.message_type == MessageType.WARNING:
            self.img_lb.setPixmap(QPixmap('src/resources/console_warning.png'))
        else:
            self.img_lb.setPixmap(QPixmap('src/resources/console_error.png'))

    def set_active(self, active: bool):
        self.active = active

        if self.active:
            self.groupBox.show()
        else:
            self.groupBox.hide()

    def is_active(self):
        return self.active

    def get_type(self):
        return self.message_type

    def get_message(self):
        return self.message

    def get_widget(self):
        return self.groupBox


class ConsoleMessageListener(QWidget, MessageListener):

    def __init__(self, parent):
        super().__init__(parent)

        self.console_stylesheet = read_stylesheet("src/resources/console.css")

        self.message_list = []
        self.button_list = []
        self.message_display = [MessageType.INFO, MessageType.DEBUG, MessageType.WARNING, MessageType.ERROR]
        self.show_console = True
        self.button_spacing = 75

        self.console_stylesheet = read_stylesheet("src/resources/console.css")
        QShortcut(QKeySequence(QtCore.Qt.Key_Space), self).activated.connect(self.on_click_close)

        self.scrollarea = QScrollArea(self)
        self.layout_SArea = None
        self.buttons_grid = QGridLayout()

        self.btn_info = QPushButton('Info', self)
        self.btn_info.setObjectName("enable")
        self.btn_info.move(355, 10)
        self.btn_info.resize(70, 35)
        self.btn_info.clicked.connect(lambda: self.on_click_button_log(MessageType.INFO))

        self.btn_debug = QPushButton('Debug', self)
        self.btn_debug.setObjectName("enable")
        self.btn_debug.move(420, 10)
        self.btn_debug.resize(70, 35)
        self.btn_debug.clicked.connect(lambda: self.on_click_button_log(MessageType.DEBUG))

        self.btn_warning = QPushButton('Warning', self)
        self.btn_warning.setObjectName("enable")
        self.btn_warning.move(485, 10)
        self.btn_warning.resize(70, 35)
        self.btn_warning.clicked.connect(lambda: self.on_click_button_log(MessageType.WARNING))

        self.btn_error = QPushButton('Error', self)
        self.btn_error.setObjectName("enable")
        self.btn_error.move(560, 10)
        self.btn_error.resize(70, 35)
        self.btn_error.clicked.connect(lambda: self.on_click_button_log(MessageType.ERROR))

        self.btn_clear = QPushButton('Clear', self)
        self.btn_clear.move(635, 10)
        self.btn_clear.resize(70, 35)
        self.btn_clear.clicked.connect(self.clear)

        self.create_scrollArea()

        self.button_list = [self.btn_info, self.btn_debug, self.btn_warning, self.btn_error, self.btn_clear]

    def create_scrollArea(self):
        self.scrollarea.setFixedSize(725, 275)
        self.scrollarea.move(10, 60)
        self.scrollarea.setWidgetResizable(True)

        widget = QWidget()
        self.scrollarea.setWidget(widget)
        self.layout_SArea = QVBoxLayout(widget)
        self.layout_SArea.addStretch(1)

    def adjust_console(self, width, height):
        self.setFixedSize(width, height)
        self.btn_clear.move(width - self.button_spacing * 2, 10)
        self.btn_error.move(width - self.button_spacing * 3, 10)
        self.btn_warning.move(width - self.button_spacing * 4, 10)
        self.btn_debug.move(width - self.button_spacing * 5, 10)
        self.btn_info.move(width - self.button_spacing * 6, 10)

        self.scrollarea.setFixedWidth(width - 20)

        # self.move(0, height)

    def draw_console(self):
        if self.show_console is False:
            return

        self.setStyleSheet(self.console_stylesheet)

        for message in self.message_list:
            widget = message.get_widget()
            if message.get_type() in self.message_display:
                if not message.is_active():
                    message.set_active(True)
                    self.layout_SArea.addWidget(widget)
                pass
            else:
                self.layout_SArea.removeWidget(widget)
                message.set_active(False)

    def paintEvent(self, event):
        if self.show_console:
            qp = QPainter(self)
            qp.setPen(QtCore.Qt.black)
            qp.setBrush(QColor(187, 187, 187))
            qp.drawRect(5, 5, self.width() - 10, self.height() - 10)

    def clear(self):
        if len(self.message_list) == 0:
            return

        for message in self.message_list:
            message.set_active(False)
            self.layout_SArea.removeWidget(message.get_widget())

        self.message_list.clear()
        self.draw_console()

    def notify(self, message: str, message_type: MessageType):
        notif = MessageConsoleContainer(message, message_type, self)
        self.message_list.append(notif)

        if notif.message_type in self.message_display:
            self.layout_SArea.addWidget(notif.get_widget())

    def set_active_button(self, active: bool):
        for button in self.button_list:
            if active:
                button.show()
            else:
                button.hide()

    def on_click_close(self):
        if self.show_console:
            self.show_console = False
        else:
            self.show_console = True

        if self.show_console:
            self.scrollarea.show()
            self.set_active_button(True)
        else:
            self.scrollarea.hide()
            self.set_active_button(False)

        self.update()

    def on_click_button_log(self, m_type: MessageType):
        if m_type in self.message_display:
            self.message_display.remove(m_type)
            self.button_list[int(m_type)].setObjectName("disable")
        else:
            self.message_display.append(m_type)
            self.button_list[int(m_type)].setObjectName("enable")

        self.draw_console()

