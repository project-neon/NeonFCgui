"""
Main window using PyQt6.
Sections: field graphics, pop-up menus,
change game status, change game settings,
game informations and robots informations.
"""

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QFont
from main_window.menu import Menu
from main_window.game_controls import GameControls
from main_window.game_settings import GameSettings
from main_window.field_graphics.field_view import FieldView
from main_window.informations import Info
from main_window.robot_info import RobotInfo
from main_window.fouls import Fouls
# from PyQt6.QtCore import QTimer, QCoreApplication

def teste():
    print("Oi :)")

class MainWindow(QMainWindow):
    def __init__(self):
        # reference to app instance?

        # Create application's GUI
        super(MainWindow, self).__init__()
        self.setWindowTitle("Neon Soccer")
        
        self.window_width = 1200
        self.window_height = 800
        self.setGeometry(100, 100, self.window_width, self.window_height)
        self.setFont(QFont('Arial', 15))

        # Organizing the layout
        # Vertical layout divided into top section
        # for controls, the field visualization in
        # the middle and a bottom section for informations.
        window_layout = QVBoxLayout()

        # Width and height of each widget
        w = int(self.window_width/2)
        h = int(self.window_height/10)
        
        # Top section with buttons
        top_h_layout = QHBoxLayout()
        top_left_collumn = QVBoxLayout()

        # Adding pop-up menus widget
        menu_widget = Menu()
        menu_widget.setMaximumHeight(h)
        menu_widget.resize(w, h)
        top_left_collumn.addWidget(menu_widget)
        
        # Adding game status controls widget
        game_controls_widget = GameControls()
        game_controls_widget.setMaximumHeight(h)
        game_controls_widget.resize(w, h)
        top_left_collumn.addWidget(game_controls_widget)

        top_h_layout.addLayout(top_left_collumn)

        h = int((h*2)+6)

        # Adding game settings widget
        game_settings_widget = GameSettings()
        game_settings_widget.setMaximumHeight(h)
        game_settings_widget.resize(w, h)
        top_h_layout.addWidget(game_settings_widget)
        window_layout.addLayout(top_h_layout)

        # Lower section with field visualization,
        # robot informations, game informations and fouls
        bottom_h_layout = QHBoxLayout()
        bottom_h_layout.addWidget(FieldView())

        # Fouls and informations sections
        right_v_layout = QVBoxLayout()
        
        # Fouls and robot informations
        right_h_layout = QHBoxLayout()
        foul_widget = Fouls()
        foul_widget.setMaximumWidth(int(self.window_width/6))
        right_h_layout.addWidget(foul_widget)
        robots_widget = RobotInfo()
        robots_widget.setMaximumWidth(int(self.window_width/3))
        right_h_layout.addWidget(robots_widget)

        right_v_layout.addLayout(right_h_layout)
        info_widget = Info()
        info_widget.setMaximumHeight(h)
        info_widget.setMaximumWidth(int(self.window_width/2))
        # info_widget.resize(w, h)
        right_v_layout.addWidget(info_widget)

        bottom_h_layout.addLayout(right_v_layout)

        window_layout.addLayout(bottom_h_layout)

        widget = QWidget()
        widget.setLayout(window_layout)
        self.setCentralWidget(widget)
