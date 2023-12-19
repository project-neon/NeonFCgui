"""
Section of the main window where the
game's status controls will be displayed.
"""

from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtGui import QPalette, QColor

class GameControls(QWidget):
    def __init__(self):
        super(GameControls, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)

        QLabel("<h1> GameControls! </h1>", parent=self)
