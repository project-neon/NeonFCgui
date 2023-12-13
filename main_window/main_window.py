"""
Main window using PyQt6.
Sections: field graphic, menus, change game status, main informations.
"""

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer, QCoreApplication
from main_window.menu import Menu
from main_window.field_graphics.field_view import FieldView

def teste():
    print("Oi :)")

class MainWindow(QMainWindow):

    def __init__(self):
        # reference to app instance?

        # Create application's GUI
        super(MainWindow, self).__init__()
        self.setWindowTitle("Neon Soccer")
        self.setGeometry(100, 100, 700, 300)

        # Organizing the layout
        # Vertical layout divided into top sections and
        # the field visualization at the bottom
        layout = QVBoxLayout()
        layout.addWidget(Menu())
        layout.addWidget(FieldView())

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
