"""
Section of the main window where the
game's setting buttons will be displayed.
"""

import os
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtGui import QPalette, QColor, QFont, QIcon

class GameSettings(QWidget):
    def __init__(self):
        super(GameSettings, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)

        self.current_color = 'blue'
        self.current_side = 'left'

        # Creating the change color and side buttons
        self.path_to_icons = os.getcwd()+"/main_window/images/"
        self.btn_change_color = QPushButton(
            icon=QIcon(self.path_to_icons+"blue.svg"), text="Alternar Cor", parent=self
        )
        self.btn_change_color.setIconSize(QSize(40, 40))
        self.btn_change_color.setFont(QFont('Arial', 15))
        self.btn_change_color.setFixedSize(180, 60)
        self.btn_change_color.clicked.connect(self.onClick)

        self.btn_change_side = QPushButton(
            icon=QIcon(self.path_to_icons+"esquerda.svg"), text="Alternar Lado", parent=self
        )
        self.btn_change_side.setIconSize(QSize(40, 40))
        self.btn_change_side.setFont(QFont('Arial', 15))
        self.btn_change_side.setFixedSize(180, 60)
        self.btn_change_side.clicked.connect(self.onClick)

        # Create game mode selection section
        top_h_layout = QHBoxLayout()
        top_h_layout.addWidget(QLabel("<h1> Modo treino / comp </h1>", parent=self))

        # Adding buttons to layout
        bottom_h_layout = QHBoxLayout()
        bottom_h_layout.addWidget(self.btn_change_color)
        # TODO alterar texto mostrando cor atual setIcon()
        # bottom_h_layout.addWidget(QLabel("<h2> Atual: x </h2>", parent=self))
        bottom_h_layout.addWidget(self.btn_change_side)
        # TODO alterar texto mostrando lado atual
        # bottom_h_layout.addWidget(QLabel("<h2> Atual: x </h2>", parent=self))

        v_layout = QVBoxLayout()
        v_layout.addLayout(top_h_layout)
        v_layout.addLayout(bottom_h_layout)

        self.setLayout(v_layout)

        # QLabel("<h1> GameSettings! </h1>", parent=self)

    def onClick(self):
        sender = self.sender()
        icon = sender.icon()

        if sender is self.btn_change_color:
            if self.current_color == 'blue':
                sender.setIcon(QIcon(self.path_to_icons+"yellow.svg"))
                self.current_color = 'yellow'
            else:
                sender.setIcon(QIcon(self.path_to_icons+"blue.svg"))
                self.current_color = 'blue'
        elif sender is self.btn_change_side:
            if self.current_side == 'left':
                sender.setIcon(QIcon(self.path_to_icons+"direita.svg"))
                self.current_side = 'right'
            else:
                sender.setIcon(QIcon(self.path_to_icons+"esquerda.svg"))
                self.current_side = 'left'
