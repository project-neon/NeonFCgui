"""
Section of the main window where the
robot's informations will be displayed.
"""

from PyQt6.QtWidgets import QLabel, QWidget, QGridLayout, QVBoxLayout, QFrame
from PyQt6.QtGui import QPalette, QColor, QFont

from entities import Match, Robot


class RobotFrame(QFrame):
    def __init__(self, id=-1):
        super(RobotFrame, self).__init__()
        self.id = id
        v_layout = QVBoxLayout()

        # Title of the section with robot id
        title = QLabel("Robô "+str(id), parent=self)
        font = QFont('Arial', 16)
        if self.id != -1:
            font.setBold(True)
        title.setFont(font)
        v_layout.addWidget(title)
        self.title = title

        # Robot's strategy
        self.strategy = "None"
        self.lbl_strategy = QLabel("Estratégia:<br/>" + self.strategy, parent=self)
        self.lbl_strategy.setWordWrap(True)
        v_layout.addWidget(self.lbl_strategy)

        # Robot's battery
        self.battery = -1
        self.lbl_battery = QLabel("Bateria:<br/>" + str(self.battery) + "%", parent=self)
        self.lbl_battery.setWordWrap(True)
        v_layout.addWidget(self.lbl_battery)

        self.setLayout(v_layout)

        # Adding border to frame
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.setLineWidth(1)

    def update_info(self, battery, strategy):
        self.strategy = strategy
        self.lbl_strategy.setText("Estratégia:<br/>" + self.strategy)
        self.battery = battery
        self.lbl_battery.setText("Bateria:<br/>" + str(self.battery) + "%")
        self.title.setText("Robô "+str(self.id))

class RobotsInfo(QWidget):
    def __init__(self, robot_num=3):
        # TODO receive list of ids instead of number of robots?
        # or maybe receive game category (EL or SSL)

        super(RobotsInfo, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)

        # Creating table of informations
        grid = QGridLayout()
        # 3 robots in a single column for EL,
        # 6 robots in 2 columns for SSL

        self.robot_list = []
        # TODO make sure robot_num > 0 and robot_num < 7
        for i in range(robot_num):
            r = RobotFrame(i)
            r.setFixedWidth(180)
            self.robot_list.append(r)

        # sets the ids according to the entities.robot id setup
        self.robot_list[0].id = 5
        self.robot_list[1].id = 7
        self.robot_list[2].id = 8

        grid.addWidget(self.robot_list[0], 0, 0)
        grid.addWidget(self.robot_list[1], 1, 0)
        grid.addWidget(self.robot_list[2], 2, 0)
        # grid.addWidget(RobotFrame(), 0, 1)
        # grid.addWidget(RobotFrame(), 1, 1)
        # grid.addWidget(RobotFrame(), 2, 1)

        self.setLayout(grid)

    def update_info(self, status: Match):
        for robot in self.robot_list:
            robot_info = status.fetch_robot_by_id(robot.id)
            if robot_info is not None:
                # TODO since there's no battery information in the API side then it cannot be imported
                robot.update_info(0,str(robot.strategy))