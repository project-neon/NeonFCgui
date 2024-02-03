"""
Section of the main window where the
pop-up menu's buttons will be displayed.
"""

from PyQt6.QtWidgets import QLabel, QWidget, QHBoxLayout, QPushButton
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

class Menu(QWidget):
    def __init__(self):
        super(Menu, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)

        h_layout = QHBoxLayout()

        # Button to open parameter settings
        self.params = QPushButton(text="Parâmetros", parent=self)
        self.params.setFixedSize(160, 60)
        h_layout.addWidget(self.params, alignment=Qt.AlignmentFlag.AlignHCenter)

        # TODO coach dropdown selection
        h_layout.addWidget(QLabel("Coach dropdown selection", parent=self), alignment=Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(h_layout)
