"""
Section of the main window where the
foul buttons will be displayed.
"""

from PyQt6.QtWidgets import QLabel, QWidget, QPushButton, QGridLayout, QHBoxLayout
from PyQt6.QtGui import QPalette, QColor, QFont
from PyQt6.QtCore import QSize, Qt

class Button(QPushButton):
    def __init__(self, text="", w=180, h=60):
        super().__init__()
        self.setText(text)
        self.setFixedSize(QSize(w, h))
        # TODO connect buttons to function onClick()?

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

        # Horizontal layout with three grids for:
        # fouls, quadrant and foul_color
        layout = QHBoxLayout()
        layout.setSpacing(20)

        # 4 foul buttons
        self.btn_free_ball = Button(text="Free Ball")
        self.btn_kickoff = Button(text="Kickoff")
        self.btn_goal_kick = Button(text="Goal Kick")
        self.btn_penalty = Button(text="Penalty Kick")

        grid = QGridLayout()
        grid.setSpacing(12)
        
        title = QLabel("Falta", parent=self)
        font = QFont('Arial', 16)
        # font.setBold(True)
        title.setFont(font)
        grid.addWidget(title, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter) # row:0, column:0, spans 1 row, spans 2 columns

        grid.addWidget(self.btn_free_ball, 1, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.btn_kickoff, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        grid.addWidget(self.btn_goal_kick, 2, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.btn_penalty, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        layout.addLayout(grid)

        # 4 quadrant buttons
        # TODO selected button?
        self.btn_q1 = Button(text='Q1', w=88)
        self.btn_q2 = Button(text='Q2', w=88)
        self.btn_q3 = Button(text='Q3', w=88)
        self.btn_q4 = Button(text='Q4', w=88)

        grid = QGridLayout()
        grid.setSpacing(12)

        title = QLabel("Quadrante", parent=self)
        font = QFont('Arial', 16)
        title.setFont(font)
        grid.addWidget(title, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter) # row:0, column:0, spans 1 row, spans 2 columns

        grid.addWidget(self.btn_q2, 1, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.btn_q1, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        grid.addWidget(self.btn_q3, 2, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.btn_q4, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        layout.addLayout(grid)

        # Foul color buttons
        # TODO leave button selected
        self.btn_blue = Button(text='blue')
        self.Btn_yellow = Button(text='yellow')

        grid = QGridLayout()
        grid.setSpacing(12)

        title = QLabel("Time", parent=self)
        font = QFont('Arial', 16)
        title.setFont(font)
        grid.addWidget(title, 0, 0, alignment=Qt.AlignmentFlag.AlignHCenter) # row:0, column:0, spans 1 row, spans 2 columns

        grid.addWidget(self.btn_blue, 1, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        grid.addWidget(self.Btn_yellow, 2, 0, alignment=Qt.AlignmentFlag.AlignHCenter)

        layout.addLayout(grid)
        
        self.setLayout(layout)
