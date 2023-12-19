"""
Main window using PyQt6.
Sections: field graphics, pop-up menus,
change game status, change game settings,
game informations and robots informations.
"""

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from main_window.menu import Menu
from main_window.game_controls import GameControls
from main_window.game_settings import GameSettings
from main_window.field_graphics.field_view import FieldView
from main_window.informations import Info
from main_window.robot_info import RobotInfo
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

        # Organizing the layout
        # Vertical layout divided into top section
        # for controls, the field visualization in
        # the middle and a bottom section for informations.
        layout = QVBoxLayout()

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
        layout.addLayout(top_h_layout)

        # Middle section with field visualization
        layout.addWidget(FieldView())

        # Bottom section with informations
        bottom_h_layout = QHBoxLayout()
        w = int(self.window_width/4)

        # Adding game informations widget
        info_widget = Info()
        info_widget.setMaximumHeight(h)
        info_widget.resize(w, h)
        bottom_h_layout.addWidget(info_widget)

        # Adding robots informations widgets
        # Change to list of robots later?
        robot1 = RobotInfo()
        robot1.setMaximumHeight(h)
        robot1.resize(w, h)
        robot2 = RobotInfo()
        robot2.setMaximumHeight(h)
        robot2.resize(w, h)
        robot3 = RobotInfo()
        robot3.setMaximumHeight(h)
        robot3.resize(w, h)
        bottom_h_layout.addWidget(robot1)
        bottom_h_layout.addWidget(robot2)
        bottom_h_layout.addWidget(robot3)

        layout.addLayout(bottom_h_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
