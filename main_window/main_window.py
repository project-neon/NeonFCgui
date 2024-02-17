"""
Main window using PyQt6.
Sections: field graphics, game controls and settings,
game informations and robots informations,
log and game mode selection.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QRadioButton, QLabel,
    QVBoxLayout, QHBoxLayout, QGridLayout
)
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt
from main_window.field_graphics.field_view import FieldView
from main_window.controls import *
from main_window.informations import *

def teste():
    print("Oi :)")

class GameMode(QWidget):
    def __init__(self):
        super(GameMode, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)

        self.mode = 'trainning'

        # Creating game mode 'checkboxes' (radio buttons)
        self.btn_trainning = QRadioButton(text="Modo de treino", parent=self)
        self.btn_trainning.toggled.connect(self.selectMode)
        self.btn_trainning.setFont(QFont('Arial', 15))
        self.btn_trainning.setStyleSheet("QRadioButton::font {spacing : 20px;}"
            "QRadioButton::indicator"
            "{"
            "width : 20px;"
            "height : 20px;"
            "}"
        )
        
        self.btn_competition = QRadioButton(text="Modo competição", parent=self)
        self.btn_competition.toggled.connect(self.selectMode)
        self.btn_competition.setFont(QFont('Arial', 15))
        self.btn_competition.setStyleSheet("QRadioButton::indicator"
            "{"
            "width : 20px;"
            "height : 20px;"
            "}"
        )

        self.btn_trainning.setChecked(True)

        mode_layout = QVBoxLayout()
        mode_layout.addWidget(QLabel("Modo", parent=self), alignment=Qt.AlignmentFlag.AlignHCenter)
        mode_layout.addWidget(self.btn_trainning)
        mode_layout.addWidget(self.btn_competition)
        self.setLayout(mode_layout)

    def selectMode(self):
        sender = self.sender()
        if sender.isChecked():
            if sender == self.btn_trainning:
                self.mode = 'trainning'
            elif sender == self.btn_competition:
                self.mode = 'competition'
            print("Mode: "+self.mode)
            # TODO display this message on log?

class MainWindow(QMainWindow):
    def __init__(self):
        # Create application's GUI
        super(MainWindow, self).__init__()
        self.setWindowTitle("Neon Soccer")
        
        self.window_width = 1200
        self.window_height = 900
        self.setGeometry(100, 100, self.window_width, self.window_height)
        self.setFont(QFont('Arial', 15))

        # Organizing the layout
        # Vertical layout divided into top section
        # for controls and a bottom section for the
        # field visualization and informations.
        window_layout = QVBoxLayout()
        
        # Top section with buttons
        top_h_layout = QHBoxLayout()
        
        # Adding game status controls widget
        game_controls_widget = GameControls()
        h = int(self.window_height/10)
        game_controls_widget.setFixedHeight(int(h*2.5))
        top_h_layout.addWidget(game_controls_widget)

        # Adding game fouls section
        fouls_widget = Fouls()
        fouls_widget.setFixedHeight(int(h*2.5))
        top_h_layout.addWidget(fouls_widget)

        window_layout.addLayout(top_h_layout)

        # Lower section with field visualization,
        # robot informations, game informations and fouls
        bottom_h_layout = QHBoxLayout()
        bottom_h_layout.addWidget(FieldView(), stretch=1)

        # GUI mode and NeonFC informations displayed
        # in a grid (10 rows, 6 columns)
        # TODO EL and SSL shall have diferent grid configurations
        grid = QGridLayout()

        # Widget to choose game mode
        mode_widget = GameMode()
        grid.addWidget(mode_widget, 0, 3, 1, 3) # starts at row:0, column:3, spans 1 row, spans 3 columns

        # NeonFC's informations
        game_info_widget = GameInfo()
        grid.addWidget(game_info_widget, 1, 3, 4, 3)

        # Log displaying errors and warning messages
        log_widget = Log()
        grid.addWidget(log_widget, 5, 3, 5, 3)

        # Robots' informations section
        # TODO adjust for 6 robots when category == SSL
        robots_widget = RobotsInfo()
        grid.addWidget(robots_widget, 0, 0, 10, 3)

        # Adding grid on a widget for better control of its alignment
        grid_widget = QWidget()
        grid_widget.setLayout(grid)

        bottom_h_layout.addWidget(grid_widget, alignment=Qt.AlignmentFlag.AlignRight)
        window_layout.addLayout(bottom_h_layout)

        widget = QWidget()
        widget.setLayout(window_layout)
        self.setCentralWidget(widget)
