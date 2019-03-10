from src.message_listener import MessageListener
from src.message_type import MessageType

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, QVBoxLayout, QPushButton, QShortcut, QScrollArea, QGroupBox
from PyQt5.QtGui import QPixmap, QPainter, QColor, QKeySequence


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

        self.message_list = []
        self.message_display = [MessageType.INFO, MessageType.DEBUG, MessageType.WARNING, MessageType.ERROR]
        self.show_console = True

        QShortcut(QKeySequence(QtCore.Qt.Key_Space), self).activated.connect(self.on_click_close) #Set a console shortcut

        self.scrollarea = QScrollArea(self)
        self.layout_SArea = None

        self.btn_info = QPushButton('Info', self)
        self.btn_info.move(355, 10)
        self.btn_info.resize(60, 35)
        self.btn_info.clicked.connect(self.on_click_info)

        self.btn_debug = QPushButton('Debug', self)
        self.btn_debug.move(420, 10)
        self.btn_debug.resize(60, 35)
        self.btn_debug.clicked.connect(self.on_click_debug)

        self.btn_warning = QPushButton('Warning', self)
        self.btn_warning.move(485, 10)
        self.btn_warning.resize(70, 35)
        self.btn_warning.clicked.connect(self.on_click_warning)

        self.btn_error = QPushButton('Error', self)
        self.btn_error.move(560, 10)
        self.btn_error.resize(70, 35)
        self.btn_error.clicked.connect(self.on_click_error)

        self.btn_clear = QPushButton('Clear', self)
        self.btn_clear.move(635, 10)
        self.btn_clear.resize(60, 35)
        self.btn_clear.clicked.connect(self.clear)

        self.btn_close = QPushButton('X', self)
        self.btn_close.move(700, 10)
        self.btn_close.resize(35, 35)
        self.btn_close.clicked.connect(self.on_click_close)

        self.create_scrollArea()
        self.setFixedSize(750, 345)

    def create_scrollArea(self):
        self.scrollarea.setFixedSize(725, 275)
        self.scrollarea.move(10, 60)
        self.scrollarea.setWidgetResizable(True)

        widget = QWidget()
        self.scrollarea.setWidget(widget)
        self.layout_SArea = QVBoxLayout(widget)
        self.layout_SArea.addStretch(1)

    def draw_console(self):
        if self.show_console is False:
            return

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
            qp.drawRect(5, 5, 735, 335)

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
        if active:
            self.btn_info.show()
            self.btn_debug.show()
            self.btn_warning.show()
            self.btn_error.show()
            self.btn_clear.show()
            self.btn_close.show()
        else:
            self.btn_info.hide()
            self.btn_debug.hide()
            self.btn_warning.hide()
            self.btn_error.hide()
            self.btn_clear.hide()
            self.btn_close.hide()

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

    def on_click_info(self):
        if MessageType.INFO in self.message_display:
            self.message_display.remove(MessageType.INFO)
        else:
            self.message_display.append(MessageType.INFO)

        self.draw_console()

    def on_click_debug(self):
        if MessageType.DEBUG in self.message_display:
            self.message_display.remove(MessageType.DEBUG)
        else:
            self.message_display.append(MessageType.DEBUG)

        self.draw_console()

    def on_click_warning(self):
        if MessageType.WARNING in self.message_display:
            self.message_display.remove(MessageType.WARNING)
        else:
            self.message_display.append(MessageType.WARNING)

        self.draw_console()

    def on_click_error(self):
        if MessageType.ERROR in self.message_display:
            self.message_display.remove(MessageType.ERROR)
        else:
            self.message_display.append(MessageType.ERROR)

        self.draw_console()
