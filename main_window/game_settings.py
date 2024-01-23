"""
Section of the main window where the
game's setting buttons will be displayed.
"""

import os
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton
from PyQt6.QtGui import QPalette, QColor, QIcon, QFont

class GameSettings(QWidget):
    def __init__(self):
        super(GameSettings, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)

        self.mode = 'trainning'
        self.current_color = 'blue'
        self.current_side = 'left'

        # Creating game mode checkboxes
        self.trainning = QRadioButton(text="Modo de treino", parent=self)
        self.trainning.toggled.connect(self.selectMode)
        self.trainning.setFont(QFont('Arial', 15))
        self.trainning.setStyleSheet("QRadioButton::font {spacing : 20px;}"
            "QRadioButton::indicator"
            "{"
            "width : 20px;"
            "height : 20px;"
            "}"
        )
        
        self.competition = QRadioButton(text="Modo competição", parent=self)
        self.competition.toggled.connect(self.selectMode)
        self.competition.setFont(QFont('Arial', 15))
        self.competition.setStyleSheet("QRadioButton::indicator"
            "{"
            "width : 20px;"
            "height : 20px;"
            "}"
        )

        self.trainning.setChecked(True)

        # Create game mode selection section
        top_h_layout = QHBoxLayout()
        top_h_layout.addWidget(self.trainning)
        top_h_layout.addWidget(self.competition)
        top_h_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_h_layout.setSpacing(70)

        # Creating the change color and side buttons
        self.path_to_icons = os.getcwd()+"/main_window/images/"
        self.btn_change_color = QPushButton(
            icon=QIcon(self.path_to_icons+"blue.svg"), text=" Alternar Cor", parent=self
        )
        self.btn_change_color.setIconSize(QSize(40, 40))
        self.btn_change_color.setFixedSize(200, 60)
        self.btn_change_color.clicked.connect(self.onClick)

        self.btn_change_side = QPushButton(
            icon=QIcon(self.path_to_icons+"left.svg"), text=" Alternar Lado", parent=self
        )
        self.btn_change_side.setIconSize(QSize(40, 40))
        self.btn_change_side.setFixedSize(200, 60)
        self.btn_change_side.clicked.connect(self.onClick)

        # Adding buttons to layout
        bottom_h_layout = QHBoxLayout()
        bottom_h_layout.addWidget(self.btn_change_color)
        bottom_h_layout.addWidget(self.btn_change_side)

        v_layout = QVBoxLayout()
        v_layout.addLayout(top_h_layout)
        v_layout.addLayout(bottom_h_layout)

        self.setLayout(v_layout)

    def onClick(self):
        sender = self.sender()

        if sender is self.btn_change_color:
            if self.current_color == 'blue':
                sender.setIcon(QIcon(self.path_to_icons+"yellow.svg"))
                self.current_color = 'yellow'
            else:
                sender.setIcon(QIcon(self.path_to_icons+"blue.svg"))
                self.current_color = 'blue'
        elif sender is self.btn_change_side:
            if self.current_side == 'left':
                sender.setIcon(QIcon(self.path_to_icons+"right.svg"))
                self.current_side = 'right'
            else:
                sender.setIcon(QIcon(self.path_to_icons+"left.svg"))
                self.current_side = 'left'
    
    def selectMode(self):
        sender = self.sender()
        if sender.isChecked():
            if sender == self.trainning:
                self.mode = 'mode: trainning'
            elif sender == self.competition:
                self.mode = 'mode: competition'
            print(self.mode)
