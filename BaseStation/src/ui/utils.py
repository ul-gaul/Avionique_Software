from PyQt5.QtWidgets import QWidget, QSizePolicy


def set_minimum_expanding_size_policy(widget: QWidget):
    set_size_policy(widget, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)


def set_fixed_size_policy(widget: QWidget):
    set_size_policy(widget, QSizePolicy.Fixed, QSizePolicy.Fixed)


def set_minimum_size_policy(widget: QWidget):
    set_size_policy(widget, QSizePolicy.Minimum, QSizePolicy.Minimum)


def set_size_policy(widget: QWidget, horizontal_policy: QSizePolicy, vertical_policy: QSizePolicy):
    size_policy = QSizePolicy(horizontal_policy, vertical_policy)
    size_policy.setHorizontalStretch(0)
    size_policy.setVerticalStretch(0)
    size_policy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
    widget.setSizePolicy(size_policy)


def read_stylesheet(path: str):
    with open(path, 'r') as f:
        return f.read()
