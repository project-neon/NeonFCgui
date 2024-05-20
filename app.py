"""
Neon Soccer GUI Application
Starts main window's thread
"""

import threading
import sys
from PyQt6.QtCore import Qt
from main_window import MainWindow
from PyQt6.QtWidgets import QApplication

class App(threading.Thread):
    def __init__(self, gui):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseDesktopOpenGL)  # <- TODO é ok eu colocar isso aqui? precisa fazer isso antes do objeto ser criado - Júlio
        self.gui = gui

        self.app = QApplication(sys.argv)

        screen_size = self.app.primaryScreen().size() # See QScreen class
        screen_width = screen_size.width()
        screen_height = screen_size.height()

        self.window = MainWindow(gui.match, screen_width, screen_height)

    def start(self):
        # Show application's GUI
        self.window.show()
        # self.window.showMaximized()
        self.app.exec()
