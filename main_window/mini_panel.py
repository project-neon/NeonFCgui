import math
import typing
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout
)
# from PyQt6.QtGui import QFont, QPalette, QColor, QIcon
from PyQt6.QtCore import Qt, QTimerEvent

from entities import Match
from main_window.widgets.field_view import FieldView
from main_window.widgets import *

class MiniPanel(QWidget):

    #TODO this is a bandaid solution and must be removed ASAP
    context: Match = None
    updatable_components = []

    def __init__(self, context: Match, window_height):
        super(MiniPanel, self).__init__()
        self.context = context
        self.window_height = window_height

        print("Categoria: MINI")

        # Organizing the layout
        # Vertical layout divided into top section
        # for controls and a bottom section for the
        # field visualization and informations.
        window_layout = QVBoxLayout()
        
        # Top section with buttons
        top_h_layout = QHBoxLayout()
        
        # Log widget displaying errors and warning messages
        self.log_widget = Log()
        self.log_widget.add_message("Categoria: MINI")
        
        # Adding game status controls widget
        self.game_controls_widget = GameControls(self.context, self.log_widget)
        h = int(self.window_height/10)
        self.game_controls_widget.setFixedHeight(int(h*2.5))
        top_h_layout.addWidget(self.game_controls_widget)
        self.updatable_components.append(self.game_controls_widget)

        # Adding game fouls section
        self.fouls_widget = Fouls(self.context, self.log_widget)
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
        grid = QGridLayout()

        # Widget to choose game mode
        self.mode_widget = GameMode(self.context, self.log_widget)
        grid.addWidget(self.mode_widget, 0, 3, 1, 3) # starts at row:0, column:3, spans 1 row, spans 3 columns

        # NeonFC's informations
        self.game_info_widget = GameInfo()
        grid.addWidget(self.game_info_widget, 1, 3, 4, 3)
        self.updatable_components.append(self.game_info_widget)

        # Add log widget to grid
        grid.addWidget(self.log_widget, 5, 3, 5, 3)

        # Robots' informations section
        self.robots_widget = RobotsInfo(self.context)
        grid.addWidget(self.robots_widget, 0, 0, 10, 3)
        self.updatable_components.append(self.robots_widget)

        # Adding grid on a widget for better control of its alignment
        grid_widget = QWidget()
        grid_widget.setLayout(grid)

        bottom_h_layout.addWidget(grid_widget, alignment=Qt.AlignmentFlag.AlignRight)
        window_layout.addLayout(bottom_h_layout)

        self.setLayout(window_layout)

        # Creates the timer that refreshes interface components periodically
        self.startTimer(math.ceil(100 / 3))

        # Initializes the match object for field rendering
        self.field_vis.setupVSSS()

    def timerEvent(self, event: typing.Optional['QTimerEvent']) -> None:
        for component in self.updatable_components:
            component.update_info(self.context)

