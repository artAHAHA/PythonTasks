import numpy as np
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class SquareWidget(QWidget):

    clicked = pyqtSignal(int)

    def __init__(self, colors, index, is_central=False):
        super().__init__()
        self.colors = colors
        self.index = index
        self.is_central = is_central
        self.setFixedSize(200, 200)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        center = self.rect().center()
        radius = min(self.width(), self.height()) // 3

        # Рисуем квадратный контур
        side = radius * 2
        top_left = QPoint(center.x() - radius, center.y() - radius)
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(QRect(top_left, QSize(side, side)))

        if not self.is_central:
            for i in range(4):
                angle = i * 90 - 45
                x = center.x() + radius * np.cos(np.radians(angle))
                y = center.y() + radius * np.sin(np.radians(angle))

                color = QColor(self.colors[i])
                painter.setBrush(color)
                painter.setPen(Qt.NoPen)
                painter.drawRect(int(x - 15), int(y - 15), 30, 30)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.index)
