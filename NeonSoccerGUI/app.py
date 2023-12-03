"""
Neon Soccer GUI Application
Starts main window's thread
"""

import threading
import sys
from main_window import MainWindow
from PyQt6.QtWidgets import QApplication

class App(threading.Thread):
    def __init__(self, gui):
        self.gui = gui
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        # self.main_window = MainWindow(self)

    def start(self):
        # self.main_window.start()

        # Show application's GUI
        self.window.show()
        self.app.exec()
