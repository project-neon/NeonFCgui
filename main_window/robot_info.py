"""
Section of the main window where the
robot's informations will be displayed.
"""

from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtGui import QPalette, QColor

class RobotInfo(QWidget):
    def __init__(self):
        super(RobotInfo, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)

        QLabel("<h1> RobotInfo! </h1>", parent=self)
