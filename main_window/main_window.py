"""
Main window using PyQt6.
Sections: field graphics, game controls and settings,
game informations and robots informations,
log and game mode selection.
"""
import math
import typing
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout
)
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon
from PyQt6.QtCore import Qt, QTimerEvent

from entities import Match
from main_window.field_graphics.field_view import FieldView
from main_window.widgets import *
from main_window.ssl_panel import SSLPanel
from main_window.mini_panel import MiniPanel

class MainWindow(QMainWindow):
    def __init__(self, context: Match, s_width = 1200, s_height = 900):
        # Create application's GUI
        super(MainWindow, self).__init__()
        self.setWindowTitle("Neon Soccer")

        self.path_to_icons = os.getcwd()+"/main_window/images/"
        icon = QIcon(self.path_to_icons+"neon_green_logo.png")
        self.setWindowIcon(icon)

        # Puts the given match as context for interface display sync
        self.context = context

        self.screen_width = s_width
        self.screen_height = s_height

        self.window_width = 1000
        self.window_height = 800
        self.setGeometry(100, 100, self.window_width, self.window_height)
        self.setFont(QFont('Arial', 15))

        self.category = None # "MINI" or "SSL"
        self.category_widget = None # MINI widget or SSL widget

        # Creating stacked widget to controw which widgets will show onscreen
        self.stacked_widget = QStackedWidget()

        # Creating category selection widget which is the first screen of the app
        self.start_widget = CategorySelect(self)
        # start_layout = QVBoxLayout()
        # start_layout.addWidget(self.start_widget)
        # self.setLayout(start_layout)

        # Adding category selection widget to stacked_widget
        self.stacked_widget.addWidget(self.start_widget)

        self.setCentralWidget(self.stacked_widget)

    def run_category_widget(self, category):
        self.category = category
        
        self.context.set_new_category(self.category)
        
        if category == "MINI":
            self.category_widget = MiniPanel(self.context, self.window_height)
        else:
            self.category_widget = SSLPanel(self.context, self.window_height)
        
        self.stacked_widget.addWidget(self.category_widget)
        self.stacked_widget.setCurrentWidget(self.category_widget)
