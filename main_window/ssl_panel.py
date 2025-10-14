import math
import typing
from PyQt6.QtWidgets import (
    QWidget, QLabel, QComboBox,
    QVBoxLayout, QHBoxLayout, QGridLayout, QSizePolicy
)
from PyQt6.QtGui import QPalette, QColor #, QIcon, QFont
from PyQt6.QtCore import Qt, QTimerEvent

from entities import Match
from main_window.widgets.field_view import FieldView
from main_window.widgets import *
from main_window.templates import TemplateWidget

class SSLPanel(QWidget):

    context: Match = None
    updatable_components = []

    def __init__(self, context: Match, s_width, s_height):
        super(SSLPanel, self).__init__()

        self.context = context
        self.screen_width = s_width
        self.screen_height = s_height

        # self.setMinimumWidth(int(self.screen_width/4))
        # self.setMaximumWidth(self.screen_width)
        # self.setMinimumHeight(int(self.screen_height/4))
        # self.setMaximumHeight(self.screen_height)
        # self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        print("Categoria: SSL")

        # Organizing the layout
        # Vertical layout divided into top section
        # for controls and a bottom section for the
        # field visualization and informations.
        window_layout = QVBoxLayout()
        
        #==================================================
        # Top section with buttons
        # top_h_layout = QHBoxLayout()
        
        # Log widget displaying errors and warning messages
        self.log_widget = Log()
        self.log_widget.add_message("Categoria: SSL")

        # Height of the top widgets
        h = int(self.screen_height/10)

        # Adding game status widget
        self.game_status_widget = GameStatus(self.context, self.log_widget, self)
        self.game_status_widget.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self.game_status_widget.setFixedHeight(int(h*0.6))
        
        # Adding game controls widget
        self.game_controls_widget = GameControls(self.context, self.log_widget, self)
        self.game_controls_widget.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        #==================================================
        # self.game_controls_widget.setFixedHeight(int(h*1.8))
        self.game_controls_widget.setFixedHeight(int(h*2.45))
        #==================================================
        # top_h_layout.addWidget(self.game_controls_widget, stretch=2)
        self.updatable_components.append(self.game_controls_widget)

        # Adding game fouls section
        self.fouls_widget = Fouls(self.context, self.log_widget, self)
        self.fouls_widget.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self.fouls_widget.setFixedHeight(int(h*1.8))
        # top_h_layout.addWidget(self.fouls_widget, stretch=2)

        # Top section with buttons
        # top_h_layout = QHBoxLayout()
        # top_v_layout = QVBoxLayout()
        #
        # top_v_layout.addWidget(self.fouls_widget)
        # top_v_layout.addWidget(self.game_status_widget)
        #
        # top_h_layout.addLayout(top_v_layout, stretch=2)
        # top_h_layout.addWidget(self.game_controls_widget, stretch=1)
        # window_layout.addLayout(top_h_layout)

        # Lower section with field visualization,
        # robot informations, game informations and fouls
        bottom_h_layout = QHBoxLayout()
        self.field_vis = FieldView(self.context)
        # bottom_h_layout.addWidget(self.field_vis, stretch=1)
        bottom_h_layout.addWidget(self.field_vis, stretch=18)

        # GUI mode and NeonFC informations displayed
        # in a grid (10 rows, 6 columns)
        # TODO place robots_info section in bottom_h_layout
        grid = QGridLayout()
        grid.setContentsMargins(0,0,0,0)
        # grid.setColumnStretch(0, 10)
        # grid.setColumnStretch(1, 1)
        # grid.setColumnStretch(2, 0)
        # grid.setColumnStretch(3, 8)
        # grid.setColumnStretch(4, 1)
        # grid.setColumnStretch(5, 0)

        # Widget to select goalkeeper by robot_id
        # self.gk_widget = GoalkeeperID(self.context, self.log_widget)
        # self.updatable_components.append(self.gk_widget)

        # grid.addWidget(self.gk_widget, 0, 3, 1, 3) # starts at row:0, column:3, spans 1 row, spans 3 columns

        # Widget to choose game mode
        # self.mode_widget = GameMode(self.context, self.log_widget)
        # grid.addWidget(self.mode_widget, 1, 3, 1, 3) # starts at row:1, column:3, spans 1 row, spans 3 columns
        # self.mode_widget = GUIMode(self.context, self.log_widget)
        # grid.addWidget(self.mode_widget, 0, 3, 1, 3) # starts at row:0, column:3, spans 1 row, spans 3 columns

        # NeonFC's informations
        # self.game_info_widget = GameInfo()
        # # grid.addWidget(self.game_info_widget, 2, 3, 3, 3)
        # grid.addWidget(self.game_info_widget, 1, 3, 4, 3)
        # self.updatable_components.append(self.game_info_widget)
        #
        # # Add log widget to grid
        # grid.addWidget(self.log_widget, 5, 3, 5, 3)

        # Robots' informations section
        self.robots_widget = RobotsInfo(self.context)
        grid.addWidget(self.robots_widget, 0, 0, 10, 3)
        # self.updatable_components.append(self.robots_widget)
        self.updatable_components.append(self.robots_widget.robots_grid)

        # Adding grid to a widget for better control of its alignment
        grid_widget = QWidget()
        grid_widget.setLayout(grid)

        # bottom_h_layout.addWidget(grid_widget, alignment=Qt.AlignmentFlag.AlignRight)
        bottom_h_layout.addWidget(grid_widget, alignment=Qt.AlignmentFlag.AlignRight, stretch=7)
        window_layout.addLayout(bottom_h_layout)

        # Adding template widget to the bottom of the screen
        # template_widget = TemplateWidget()
        # window_layout.addWidget(template_widget)

        self.setLayout(window_layout)

        # Creates the timer that refreshes interface components periodically
        self.startTimer(math.ceil(100 / 3))
        
        # Initializes the match object for field rendering
        self.field_vis.setupSSL()

    def timerEvent(self, event: typing.Optional['QTimerEvent']) -> None:
        for component in self.updatable_components:
            component.update_info(self.context)
