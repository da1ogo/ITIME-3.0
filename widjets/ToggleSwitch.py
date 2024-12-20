from PyQt5 import  QtGui, QtWidgets
from PyQt5.QtCore import Qt, QRect


class ToggleSwitch(QtWidgets.QPushButton):
    def __init__(self,
        parent=None,
        on_text="On",
        off_text="Off"
    ) -> None:
        super().__init__(parent)

        self.on_text = on_text
        self.off_text = off_text

        self.setMinimumWidth(40)
        self.setMinimumHeight(30)

        self.setCheckable(True)

    def paintEvent(self, event):
        label = self.on_text if self.isChecked() else self.off_text
        bg_color = QtGui.QColor(190,102,114) if self.isChecked() else QtGui.QColor(255,222,193)

        radius = 15
        width = 30
        center = self.rect().center()

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(center)
        
        pen = QtGui.QPen(QtGui.QColor(190, 102, 114))
        pen2 = QtGui.QPen(bg_color)
        pen.setWidth(3)
        pen2.setWidth(1)
        painter.setPen(pen)

        painter.drawRoundedRect(QRect(-width, -radius, 2*width, 2*radius), radius, radius)
        painter.setBrush(QtGui.QBrush(bg_color))
        painter.setPen(pen2)
        sw_rect = QRect(-2*radius + width, -radius + 3, 2*radius - 6, 2*radius - 6)
        if not self.isChecked():
            sw_rect.moveLeft(-width + 6)
        painter.drawRoundedRect(sw_rect, radius, radius)
        painter.drawText(sw_rect, Qt.AlignCenter, label)
