"""
Section of the main window where the
robot's informations will be displayed.
"""

from PyQt6.QtWidgets import QLabel, QWidget, QGridLayout, QVBoxLayout, QFrame
from PyQt6.QtGui import QPalette, QColor, QFont

from entities import Match, Robot


class RobotFrame(QFrame):
    def __init__(self, robot):
        super(RobotFrame, self).__init__()
        self.id = robot.robot_id
        v_layout = QVBoxLayout()

        # Title of the section with robot id
        title = QLabel("Robô "+str(self.id), parent=self)
        font = QFont('Arial', 16)
        if self.id != -1:
            font.setBold(True)
        title.setFont(font)
        v_layout.addWidget(title)
        self.title = title

        # Robot's strategy
        self.strategy = 'None'
        if robot.strategy != None:
            self.strategy = robot.strategy
        self.lbl_strategy = QLabel("Estratégia:<br/>" + str(self.strategy), parent=self)
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
    def __init__(self, context):
        super(RobotsInfo, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)

        # Creating table of informations
        grid = QGridLayout()
        # 3 robots in a single column for Mini,
        # 6 robots in 2 columns for SSL

        self.robot_list = []    # stores match's robot list
        self.robot_frames = []  # stores a RobotFrame instance for each robot in match

        if context.robots != []:
            self.robot_list = context.robots
        else:
            # show 3 robot frames for Mini and 6 robot frames for SSL
            num_robots = 3  # 6 if category is SSL
            for i in range(num_robots):
                self.robot_list.append(Robot(-1))

        for i in range(len(self.robot_list)):
            r = RobotFrame(self.robot_list[i])
            r.setFixedWidth(180)
            self.robot_frames.append(r)

        grid.addWidget(self.robot_frames[0], 0, 0)
        grid.addWidget(self.robot_frames[1], 1, 0)
        grid.addWidget(self.robot_frames[2], 2, 0)
        # TODO implement other robots for SSL category
        # grid.addWidget(RobotFrame(), 0, 1)
        # grid.addWidget(RobotFrame(), 1, 1)
        # grid.addWidget(RobotFrame(), 2, 1)

        self.setLayout(grid)

    def update_info(self, status: Match):
        for robot in self.robot_frames:
            robot_info = status.fetch_robot_by_id(robot.id)
            if robot_info is not None:
                # TODO since there's no battery information in the API side then it cannot be imported
                robot.update_info(0,str(robot.strategy))