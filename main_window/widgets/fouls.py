"""
Section of the main window where the
foul buttons will be displayed.
"""

from PyQt6.QtWidgets import (
    QLabel, QWidget, QPushButton, QSpacerItem,
    QGridLayout, QHBoxLayout, QSizePolicy
)
from PyQt6.QtGui import QPalette, QColor, QFont
from PyQt6.QtCore import QSize, Qt
from main_window.widgets.log import Log
from entities.match import Match

class Fouls(QWidget):
    def __init__(self, context: Match, log: Log, parent_panel):
        super(Fouls, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#36313C'))
        self.setPalette(palette)

        self.setStyleSheet("QPushButton:checked{background-color: rgb(140, 140, 140);}")
        # TODO change styleSheet's font family, font size and QPushButton default size

        self.context = context
        self.log=log
        self.parent_panel = parent_panel

        self.parent_width = self.parent_panel.width()
        self.parent_height = self.parent_panel.height()

        self.foul_color = 'blue'
        self.quadrant = 1
        self.foul_name = ""

        # Horizontal layout with three grids for:
        # fouls, quadrants and foul colors
        layout = QHBoxLayout()
        # layout.setSpacing(24)
        layout.setSpacing(32)

        # button sizing configurations:
        w = int(self.parent_width/(1.2))
        h = int(self.parent_height/(2.4))
        
        btn_size = QSize(int(w/(5)), int(h/4))
        btn_size_small = QSize(int(w/(9)), int(h/4))
        font_size = int(h/16)

        # 4 foul buttons
        self.btn_free_ball = QPushButton(text="Free Ball")
        self.btn_free_ball.clicked.connect(self.change_foul)

        self.btn_kickoff = QPushButton(text="Kickoff")
        self.btn_kickoff.clicked.connect(self.change_foul)

        self.btn_goal_kick = QPushButton(text="Goal Kick")
        self.btn_goal_kick.clicked.connect(self.change_foul)

        self.btn_penalty = QPushButton(text="Penalty Kick")
        self.btn_penalty.clicked.connect(self.change_foul)

        for btn in [self.btn_free_ball, self.btn_kickoff, self.btn_goal_kick, self.btn_penalty]:
            btn.setMinimumSize(btn_size)
            btn.setMaximumHeight(btn_size.height())
            btn.setFont(QFont('Arial', font_size))
            btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        grid = QGridLayout()
        grid.setSpacing(12)
        
        title = QLabel("Falta", parent=self)
        font = QFont('Arial', 16)
        # font.setBold(True)
        title.setFont(font)
        grid.addWidget(title, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter) # row:0, column:0, spans 1 row, spans 2 columns

        grid.addWidget(self.btn_free_ball, 1, 0)
        grid.addWidget(self.btn_kickoff, 1, 1)
        grid.addWidget(self.btn_goal_kick, 2, 0)
        grid.addWidget(self.btn_penalty, 2, 1)

        layout.addLayout(grid, stretch=6)

        # 4 quadrant buttons
        self.btn_q1 = QPushButton(text='1')
        self.btn_q1.setCheckable(True)
        self.btn_q1.setChecked(True)
        self.btn_q1.clicked.connect(self.change_quadrant)

        self.btn_q2 = QPushButton(text='2')
        self.btn_q2.setCheckable(True)
        self.btn_q2.clicked.connect(self.change_quadrant)

        self.btn_q3 = QPushButton(text='3')
        self.btn_q3.setCheckable(True)
        self.btn_q3.clicked.connect(self.change_quadrant)

        self.btn_q4 = QPushButton(text='4')
        self.btn_q4.setCheckable(True)
        self.btn_q4.clicked.connect(self.change_quadrant)

        for btn in [self.btn_q1, self.btn_q2, self.btn_q3, self.btn_q4]:
            # btn.setFixedSize(btn_size_small) # Better not use fixed size with size policy
            btn.setMinimumSize(btn_size_small)
            btn.setMaximumHeight(btn_size.height())
            btn.setFont(QFont('Arial', font_size))
            btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        grid = QGridLayout()
        grid.setSpacing(12)

        title = QLabel("Quadrante", parent=self)
        font = QFont('Arial', 16)
        title.setFont(font)
        grid.addWidget(title, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter) # row:0, column:0, spans 1 row, spans 2 columns

        grid.addWidget(self.btn_q2, 1, 0)
        grid.addWidget(self.btn_q1, 1, 1)
        grid.addWidget(self.btn_q3, 2, 0)
        grid.addWidget(self.btn_q4, 2, 1)

        layout.addLayout(grid, stretch=4)

        # Foul color buttons
        self.btn_blue = QPushButton(text='Azul')
        self.btn_blue.setCheckable(True)
        self.btn_blue.setChecked(True)
        self.btn_blue.clicked.connect(self.change_color)

        self.btn_yellow = QPushButton(text='Amarelo')
        self.btn_yellow.setCheckable(True)
        self.btn_yellow.clicked.connect(self.change_color)

        for btn in [self.btn_blue, self.btn_yellow]:
            btn.setMinimumSize(btn_size)
            btn.setMaximumHeight(btn_size.height())
            btn.setFont(QFont('Arial', font_size))
            btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        grid = QGridLayout()
        grid.setSpacing(12)

        title = QLabel("Time", parent=self)
        font = QFont('Arial', 16)
        title.setFont(font)
        grid.addWidget(title, 0, 0, alignment=Qt.AlignmentFlag.AlignHCenter) # row:0, column:0, spans 1 row, spans 2 columns

        grid.addWidget(self.btn_blue, 1, 0)
        grid.addWidget(self.btn_yellow, 2, 0)

        layout.addLayout(grid, stretch=3)
        
        self.setLayout(layout)
    
    def change_foul(self):
        sender = self.sender()
        if sender == self.btn_free_ball:
            self.foul_name = 'FREE_BALL'
        elif sender == self.btn_kickoff:
            self.foul_name = 'KICKOFF'
        elif sender == self.btn_goal_kick:
            self.foul_name = 'GOAL_KICK'
        elif self.btn_penalty:
            self.foul_name = 'PENALTY'
        self.context.set_game_status(self.foul_name)

        # Add foul to log
        if self.foul_color == 'blue':
            color = "Azul"
        else:
            color = "Amarelo"
        self.log.add_message(
            "Falta \'" + str(self.foul_name)
            + "\' no quadrante " + str(self.quadrant)
            + " para o time " + str(color) + "."
        )
    
    def change_quadrant(self):
        self.btn_q1.setChecked(False)
        self.btn_q2.setChecked(False)
        self.btn_q3.setChecked(False)
        self.btn_q4.setChecked(False)

        sender = self.sender()
        sender.setChecked(True)
        self.quadrant = int(sender.text())
        self.context.set_foul_quadrant(self.quadrant)

        self.log.add_message("Quadrante selecionado: " + str(self.quadrant))
    
    def change_color(self):
        sender = self.sender()
        if sender == self.btn_blue:
            self.btn_blue.setChecked(True)
            self.btn_yellow.setChecked(False)
            self.foul_color = 'blue'
            self.log.add_message("Cor da falta selecionada: Azul")
        else:
            self.btn_blue.setChecked(False)
            self.btn_yellow.setChecked(True)
            self.foul_color = 'yellow'
            self.log.add_message("Cor da falta selecionada: Amarelo")
        self.context.set_foul_color(self.foul_color)
