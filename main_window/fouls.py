"""
Section of the main window where the
game's foul controls will be displayed.
"""

import os
from PyQt6.QtWidgets import QLabel, QWidget, QPushButton, QGridLayout
from PyQt6.QtGui import QPalette, QColor, QFont, QIcon
from PyQt6.QtCore import QSize, Qt

class Button(QPushButton):
    def __init__(self, text="", w=180, h=50):
        super().__init__()
        self.setText(text)
        self.setFixedSize(QSize(w, h))
        # TODO connect buttons to onClick()

class Fouls(QWidget):
    def __init__(self):
        super(Fouls, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)

        self.foul_color = 'blue'
        self.quadrant = 1
        self.foul_name = ""

        grid = QGridLayout()
        
        title = QLabel("Faltas", parent=self)
        font = QFont('Arial', 16)
        font.setBold(True)
        title.setFont(font)
        grid.addWidget(title, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter) # row:0, column:0, spans 1 row, spans 2 columns

        # Creating the buttons
        # To add icon to the button we will use the QIcon object, which
        # gets the path to an SVG image
        self.path_to_icons = os.getcwd()+"/main_window/images/"

        # Team color for foul
        self.btn_color = QPushButton(icon=QIcon(self.path_to_icons+"blue.svg"), text=" Cor do time", parent=self)
        self.btn_color.setIconSize(QSize(30, 30))
        self.btn_color.setFixedSize(180, 60)
        self.btn_color.clicked.connect(self.onClick)
        
        # Foul buttons
        self.btn_free_ball = Button(text="Free Ball")
        self.btn_kickoff = Button(text="Kickoff")
        self.btn_goal_kick = Button(text="Goal Kick")
        self.btn_penalty = Button(text="Penalty")

        # Quadrant buttons
        self.btn_q1 = Button(text='Q1', w=88)
        self.btn_q2 = Button(text='Q2', w=88)
        self.btn_q3 = Button(text='Q3', w=88)
        self.btn_q4 = Button(text='Q4', w=88)

        # Adding buttons to layout
        grid.addWidget(self.btn_kickoff, 1, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
        grid.addWidget(self.btn_free_ball, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
        grid.addWidget(self.btn_goal_kick, 3, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
        grid.addWidget(self.btn_penalty, 4, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter)

        grid.addWidget(QLabel("Time", parent=self), 5, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
        grid.addWidget(self.btn_color, 6, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter)

        grid.addWidget(QLabel("Quadrante", parent=self), 7, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
        grid.addWidget(self.btn_q2, 8, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.btn_q1, 8, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        grid.addWidget(self.btn_q3, 9, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.btn_q4, 9, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.setLayout(grid)

    def onClick(self):
        sender = self.sender()

        if sender is self.btn_color:
            if self.foul_color == 'blue':
                sender.setIcon(QIcon(self.path_to_icons+"yellow.svg"))
                self.foul_color = 'yellow'
            else:
                sender.setIcon(QIcon(self.path_to_icons+"blue.svg"))
                self.foul_color = 'blue'
        # elif for other buttons