"""
Section of the GUI where the field will be displayed.
"""
 
from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtGui import QPalette, QColor

class FieldView(QWidget):
    def __init__(self):
        super(FieldView, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('green'))
        self.setPalette(palette)

        QLabel("<h1>Campo!</h1>", parent=self)
