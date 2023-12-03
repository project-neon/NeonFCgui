"""
Section of the main window where the
pop-up menu's buttons will be displayed.
"""

from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtGui import QPalette, QColor

class Menu(QWidget):
    def __init__(self):
        super(Menu, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('purple'))
        self.setPalette(palette)

        QLabel("<h1>Menus!</h1>", parent=self)
