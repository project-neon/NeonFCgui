"""
Section of the main window where the
game's status controls will be displayed.
"""

import os
from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt6.QtGui import QPalette, QColor, QFont, QIcon
from PyQt6.QtCore import QSize

class GameControls(QWidget):
    def __init__(self):
        super(GameControls, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)

        # Creating the PLAY, HALT and RESET buttons
        # To add icon to the button we will use the QIcon object, which
        # gets the path to an SVG image
        path_to_icons = os.getcwd()+"/main_window/images/"

        btn_start = QPushButton(icon=QIcon(path_to_icons+"start.svg"), text="START", parent=self)
        btn_start.setIconSize(QSize(50, 50))
        btn_start.setFont(QFont('Arial', 15))
        btn_start.setFixedSize(160, 60)

        btn_halt = QPushButton(icon=QIcon(path_to_icons+"halt.svg"), text="HALT", parent=self)
        btn_halt.setIconSize(QSize(50, 50))
        btn_halt.setFont(QFont('Arial', 15))
        btn_halt.setFixedSize(160, 60)
        
        btn_reset = QPushButton(icon=QIcon(path_to_icons+"Reset_1.svg"), text="RESET", parent=self)
        btn_reset.setIconSize(QSize(50, 50))
        btn_reset.setFont(QFont('Arial', 15))
        btn_reset.setFixedSize(160, 60)

        # Adding buttons to layout
        layout = QHBoxLayout()
        layout.addWidget(btn_start)
        layout.addWidget(btn_halt)
        layout.addWidget(btn_reset)
        self.setLayout(layout)
