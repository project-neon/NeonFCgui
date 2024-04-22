"""
Main window using PyQt6.
Sections: field graphics, game controls and settings,
game informations and robots informations,
log and game mode selection.
"""
import math
import typing

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel,
    QVBoxLayout, QHBoxLayout, QGridLayout
)
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt, QTimerEvent

from entities import Match
from main_window.field_graphics.field_view import FieldView
from main_window.widgets import *

class MainWindow(QMainWindow):

    #TODO this is a bandaid solution and must be removed ASAP
    context: Match = None
    updatable_components = []

    def __init__(self, context: Match, s_width = 1200, s_height = 900):
        # Create application's GUI
        super(MainWindow, self).__init__()
        self.setWindowTitle("Neon Soccer")

        # Puts the given match as context for interface display sync
        self.context = context

        self.screen_width = s_width
        self.screen_height = s_height
        
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
        
        # Log widget displaying errors and warning messages
        self.log_widget = Log()
        
        # Adding game status controls widget
        self.game_controls_widget = GameControls(self.context, self.log_widget)
        h = int(self.window_height/10)
        self.game_controls_widget.setFixedHeight(int(h*2.5))
        top_h_layout.addWidget(self.game_controls_widget)

        # Adding game fouls section
        self.fouls_widget = Fouls()
        self.fouls_widget.setFixedHeight(int(h*2.5))
        top_h_layout.addWidget(self.fouls_widget)

        window_layout.addLayout(top_h_layout)

        # Lower section with field visualization,
        # robot informations, game informations and fouls
        bottom_h_layout = QHBoxLayout()
        self.field_vis = FieldView(self.context)
        bottom_h_layout.addWidget(self.field_vis, stretch=1)

        # GUI mode and NeonFC informations displayed
        # in a grid (10 rows, 6 columns)
        # TODO EL and SSL shall have diferent grid configurations
        grid = QGridLayout()

        # Widget to choose game mode
        self.mode_widget = GameMode()
        grid.addWidget(self.mode_widget, 0, 3, 1, 3) # starts at row:0, column:3, spans 1 row, spans 3 columns

        # NeonFC's informations
        self.game_info_widget = GameInfo()
        grid.addWidget(self.game_info_widget, 1, 3, 4, 3)
        self.updatable_components.append(self.game_info_widget)

        # Add log widget to grid
        grid.addWidget(self.log_widget, 5, 3, 5, 3)

        # Robots' informations section
        # TODO adjust for 6 robots when category == SSL
        self.robots_widget = RobotsInfo()
        grid.addWidget(self.robots_widget, 0, 0, 10, 3)
        self.updatable_components.append(self.robots_widget)

        # Adding grid on a widget for better control of its alignment
        grid_widget = QWidget()
        grid_widget.setLayout(grid)

        bottom_h_layout.addWidget(grid_widget, alignment=Qt.AlignmentFlag.AlignRight)
        window_layout.addLayout(bottom_h_layout)

        widget = QWidget()
        widget.setLayout(window_layout)
        self.setCentralWidget(widget)

        # Creates the timer that refreshes interface components periodically
        self.startTimer(math.ceil(100 / 3))

    def timerEvent(self, event: typing.Optional['QTimerEvent']) -> None:
        for component in self.updatable_components:
            component.update_info(self.context)
