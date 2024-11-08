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
        self.robot = robot
        self.id = robot.robot_id
        self.team = robot.team
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

    def update_info(self):
        if self.robot.playing:
            if self.robot.strategy == None:
                    self.strategy = 'None'
            else:
                self.strategy = self.robot.strategy

            if self.robot.battery == None:
                self.battery = '-1'
            else:
                self.battery = self.robot.battery
            self.lbl_strategy.setText("Estratégia:<br/>" + str(self.strategy))
            self.lbl_battery.setText("Bateria:<br/>" + str(self.battery) + "%")
            self.title.setText("Robô "+str(self.id))

class RobotsInfo(QWidget):
    def __init__(self, context: Match):
        super(RobotsInfo, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)

        self.context = context

        # Creating table of informations
        self.grid = QGridLayout()
        # 3 robots in a single column for Mini,
        # 6 robots in 2 columns for SSL

        self.robot_list = []    # stores match's robot list
        self.robot_frames = []  # stores a RobotFrame instance for each robot in match

        # TODO fix match's categories
        if context.robots != [] and self.context.category == "MINI":
            self.robot_list = context.robots
        else:
            self.robot_list = context.robots

        print(len(self.robot_list))
        for i in range(len(self.robot_list)):
            r = RobotFrame(self.robot_list[i])
            r.setFixedWidth(180)
            self.robot_frames.append(r)

        self.show_ids = []
        self.widget_ids = []

        self.grid.addWidget(self.robot_frames[0], 0, 0)
        self.show_ids.append(self.robot_frames[0].id)
        self.widget_ids.append((self.robot_frames[0].id, 0, 0))
        self.grid.addWidget(self.robot_frames[1], 1, 0)
        self.show_ids.append(self.robot_frames[1].id)
        self.widget_ids.append((self.robot_frames[1].id, 0, 1))
        self.grid.addWidget(self.robot_frames[2], 2, 0)
        self.show_ids.append(self.robot_frames[2].id)
        self.widget_ids.append((self.robot_frames[2].id, 0, 2))
        if self.context.category == "SSL":
            self.grid.addWidget(self.robot_frames[3], 0, 1)
            self.show_ids.append(self.robot_frames[3].id)
            self.widget_ids.append((self.robot_frames[3].id, 1, 0))
            self.grid.addWidget(self.robot_frames[4], 1, 1)
            self.show_ids.append(self.robot_frames[4].id)
            self.widget_ids.append((self.robot_frames[4].id, 1, 1))
            self.grid.addWidget(self.robot_frames[5], 2, 1)
            self.show_ids.append(self.robot_frames[5].id)
            self.widget_ids.append((self.robot_frames[5].id, 1, 2))

        

        self.setLayout(self.grid)

    def update_info(self, status: Match):
        for robot in status.robots:
            if robot.playing == True and robot.robot_id not in self.show_ids:
                self.show_ids.pop(0)
                self.show_ids.append(robot.robot_id)
        for robot in self.robot_frames:

            if robot.id in self.show_ids:
                i = 0
                while i < len(self.widget_ids):
                    if self.widget_ids[i][0] not in self.show_ids and robot.id != self.widget_ids[i][0]:
                        self.grid.addWidget(robot, self.widget_ids[i][1], self.widget_ids[i][2])
                        self.widget_ids.append((robot.id, self.widget_ids[i][1], self.widget_ids[i][2]))
                        self.widget_ids.pop(i)
                        i += len(self.widget_ids)
                    i += 1

            if robot.id not in self.show_ids:
                robot.setParent(None)
            robot_info = status.fetch_robot_by_id(robot.team, robot.id)
            if robot_info is not None:
                robot.update_info()