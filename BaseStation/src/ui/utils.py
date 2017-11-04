from PyQt5.QtWidgets import QWidget, QSizePolicy


def set_minimum_expanding_size_policy(widget: QWidget):
    size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
    size_policy.setHorizontalStretch(0)
    size_policy.setVerticalStretch(0)
    size_policy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
    widget.setSizePolicy(size_policy)
