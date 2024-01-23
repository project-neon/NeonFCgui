"""
Section of the main window where the
game's informations will be displayed.
"""

from PyQt6.QtWidgets import QLabel, QWidget, QGridLayout
from PyQt6.QtGui import QPalette, QColor, QFont

class Info(QWidget):
    def __init__(self):
        super(Info, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)

        # Create information table
        grid = QGridLayout()

        # Title of the section
        title = QLabel("Informações NeonFC", parent=self)
        font = QFont('Arial', 20)
        font.setBold(True)
        title.setFont(font)
        grid.addWidget(title, 0, 0, 1, 2)

        # Game status
        status_title = QLabel("Status atual: ")
        self.status_value = QLabel("None")
        grid.addWidget(status_title, 1, 0)
        grid.addWidget(self.status_value, 1, 1)

        # Coach
        coach_title = QLabel("Coach atual: ")
        grid.addWidget(coach_title, 2, 0)
        self.current_coach = QLabel("None")
        grid.addWidget(self.current_coach, 2, 1)

        # NeonFC's update rate
        grid.addWidget(QLabel("Taxa de atualização: "), 3, 0)
        self.update_rate = QLabel("0")
        grid.addWidget(self.update_rate, 3, 1)

        self.setLayout(grid)
