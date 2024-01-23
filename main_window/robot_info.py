"""
Section of the main window where the
robot's informations will be displayed.
"""

from PyQt6.QtWidgets import QLabel, QWidget, QGridLayout
from PyQt6.QtGui import QPalette, QColor, QFont

class RobotInfo(QWidget):
    def __init__(self, id=-1):
        super(RobotInfo, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)

        # Creating table of informations
        grid = QGridLayout()

        # Title of the section with robot id
        self.robot_id = id
        title = QLabel("Robô "+str(id), parent=self)
        font = QFont('Arial', 20)
        font.setBold(True)
        title.setFont(font)
        grid.addWidget(title, 0, 0, 1, 2)
        # grid.addWidget(QLabel("Robô "+str(id), parent=self).setFont(font), 0, 0, 1, 2)

        # Robot's strategy
        grid.addWidget(QLabel("Estratégia: "), 2, 0)
        self.strategy = "None"
        self.lbl_strategy = QLabel(self.strategy, parent=self)
        grid.addWidget(self.lbl_strategy, 2, 1)

        # Robot's battery
        grid.addWidget(QLabel("Bateria: "), 3, 0)
        self.battery = -1
        self.lbl_battery = QLabel(str(self.battery), parent=self)
        grid.addWidget(self.lbl_battery, 3, 1)

        # Adding a dummy label at the second row to ensure the right size on this empty row
        # https://forum.qt.io/topic/84946/gridlayout-with-equal-sized-cells/2
        grid.addWidget(QLabel(" "), 1, 0)

        self.setLayout(grid)
