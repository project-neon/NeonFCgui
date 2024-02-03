"""
Section of the main window where the
robot's informations will be displayed.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QWidget, QGridLayout, QVBoxLayout, QFrame
from PyQt6.QtGui import QPalette, QColor, QFont

class Robot(QFrame):
    def __init__(self, id=-1):
        super(Robot, self).__init__()
        self.id = id
        v_layout = QVBoxLayout()

        # Title of the section with robot id
        title = QLabel("Robô "+str(id), parent=self)
        font = QFont('Arial', 20)
        if self.id != -1:
            font.setBold(True)
        title.setFont(font)
        v_layout.addWidget(title)

        # Robot's strategy
        self.strategy = "None"
        self.lbl_strategy = QLabel("Estratégia: " + self.strategy, parent=self)
        self.lbl_strategy.setWordWrap(True)
        v_layout.addWidget(self.lbl_strategy)

        # Robot's battery
        self.battery = -1
        self.lbl_battery = QLabel("Bateria: " + str(self.battery) + "%", parent=self)
        self.lbl_battery.setWordWrap(True)
        v_layout.addWidget(self.lbl_battery)

        self.setLayout(v_layout)

        # Adding border to frame
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.setLineWidth(1)

class RobotInfo(QWidget):
    def __init__(self, robot_num=3):
        # TODO receive list of ids instead of number of robots

        super(RobotInfo, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)

        # Creating table of informations
        grid = QGridLayout()

        self.robot_list = []
        # TODO make sure robot_num > 0 and robot_num < 7
        for i in range(robot_num):
            r = Robot(i)
            self.robot_list.append(r)
        
        grid.addWidget(self.robot_list[0], 0, 0)
        grid.addWidget(self.robot_list[1], 1, 0)
        grid.addWidget(self.robot_list[2], 2, 0)
        grid.addWidget(Robot(), 0, 1)
        grid.addWidget(Robot(), 1, 1)
        grid.addWidget(Robot(), 2, 1)
        
        self.setLayout(grid)
