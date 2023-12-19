"""
Section of the main window where the
game's setting buttons will be displayed.
"""

from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtGui import QPalette, QColor

class GameSettings(QWidget):
    def __init__(self):
        super(GameSettings, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)

        QLabel("<h1> GameSettings! </h1>", parent=self)
