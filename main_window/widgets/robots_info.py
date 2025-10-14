"""
Section of the main window where the
robot's informations will be displayed.
"""

import os
from PyQt6.QtWidgets import QLabel, QWidget, QGridLayout, QVBoxLayout, QFrame, QScrollArea
from PyQt6.QtGui import QPalette, QColor, QFont, QPixmap
from PyQt6.QtCore import Qt
from entities import Match, Robot

class RobotFrame(QFrame):
    def __init__(self, robot, team_color):
        super(RobotFrame, self).__init__()
        self.robot = robot
        self.id = robot.robot_id
        self.team = robot.team

        self.path_to_icons = os.getcwd()+"/main_window/images/"
        self.path_to_tags = os.getcwd()+"/main_window/images/tags/"

        big_font = QFont('Arial', 15)
        small_font = QFont('Arial', 12)
        small_font_bold = QFont('Arial', 12)
        small_font_bold.setBold(True)
        if self.id != -1:
            big_font.setBold(True)

        # Robot ID
        self.title = QLabel("Robô "+str(self.id), parent=self)
        self.title.setFont(big_font)

        # Robot icon
        # To add icon we will use the QPixmap object, which
        # gets the path to a png image
        if self.id != -1:
            if self.id < 10:
                num = "0" + str(self.id)
            else:
                num = str(self.id)
            tag_img = QPixmap(self.path_to_tags + str(team_color) + "_" + num + ".png")
        else:
            tag_img = QPixmap(self.path_to_tags + "robot.png")
        tag_img = tag_img.scaled(30, 30, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio, transformMode=Qt.TransformationMode.SmoothTransformation)
        self.img_lbl_tag = QLabel()
        self.img_lbl_tag.setPixmap(tag_img)
        # self.img_lbl_tag.setScaledContents(True)
        self.img_lbl_tag.setFixedSize(30, 30)

        # Robot's strategy
        self.strategy = 'None'
        if robot.strategy != None:
            self.strategy = robot.strategy
        self.lbl_strategy_title = QLabel("Estratégia:")
        self.lbl_strategy_title.setFont(small_font_bold)
        self.lbl_strategy = QLabel("  " + str(self.strategy))
        self.lbl_strategy.setFont(small_font)
        # self.lbl_strategy = QLabel("Estratégia:<br/>" + str(self.strategy), parent=self)
        # self.lbl_strategy.setWordWrap(True)

        # Robot's kicker
        self.kicker = "Sem informação"
        if robot.kicker:
            self.kicker = robot.kicker
        self.lbl_kicker_title = QLabel("Kicker:")
        self.lbl_kicker_title.setFont(small_font_bold)
        self.lbl_kicker = QLabel("  " + str(self.kicker))
        self.lbl_kicker.setFont(small_font)

        # Robot's battery
        self.battery = -1
        if robot.battery:
            self.battery = robot.battery
        battery_img = QPixmap(self.path_to_icons + "battery_icon.png")
        battery_img = battery_img.scaled(30, 30, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio, transformMode=Qt.TransformationMode.SmoothTransformation)
        self.img_lbl_battery = QLabel()
        self.img_lbl_battery.setPixmap(battery_img)
        # self.img_lbl_battery.setScaledContents(True)
        self.img_lbl_battery.setFixedSize(30, 30)
        self.lbl_battery = QLabel(str(self.battery)) # TODO add measurement unit?
        self.lbl_battery.setFont(small_font)

        # Robot's communication WiFi signal
        self.signal = -1
        if robot.signal:
            self.signal = robot.signal
        signal_img = QPixmap(self.path_to_icons + "signal_icon.png")
        signal_img = signal_img.scaled(30, 30, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio, transformMode=Qt.TransformationMode.SmoothTransformation)
        self.img_lbl_signal = QLabel()
        self.img_lbl_signal.setPixmap(signal_img)
        # self.img_lbl_signal.setScaledContents(True)
        self.img_lbl_signal.setFixedSize(30, 30)
        self.lbl_signal = QLabel(str(self.signal)) # TODO add measurement unit?
        self.lbl_signal.setFont(small_font)

        # Frame's grid layout
        self.grid = QGridLayout()
        self.grid.addWidget(self.title, 0, 0, 1, 3) # starts at row:0, column:0, spans 1 row, spans 3 columns
        self.grid.addWidget(self.img_lbl_tag, 0, 4, 1, 1) # starts at row:0, column:0, spans 1 row, spans 1 column
        self.grid.addWidget(self.lbl_strategy_title, 1, 0, 1, 5)
        self.grid.addWidget(self.lbl_strategy, 2, 0, 1, 5)
        self.grid.addWidget(self.lbl_kicker_title, 3, 0, 1, 5)
        self.grid.addWidget(self.lbl_kicker, 4, 0, 1, 5)
        self.grid.addWidget(self.img_lbl_battery, 5, 0, 1, 1)
        self.grid.addWidget(self.lbl_battery, 5, 1, 1, 1)
        self.grid.addWidget(self.img_lbl_signal, 5, 3, 1, 1)
        self.grid.addWidget(self.lbl_signal, 5, 4, 1, 1)

        self.setLayout(self.grid)

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
            if self.robot.signal == None:
                self.signal = '-1'
            else:
                self.signal = self.robot.signal
            # TODO update kicker status

            self.lbl_strategy.setText("Estratégia:<br/>" + str(self.strategy))
            self.lbl_battery.setText("Bateria:" + str(self.battery) + "%<br/>" + "Sinal:"+ str(self.signal) + "dBm")
            self.title.setText("Robô "+str(self.id))

class RobotsGrid(QWidget):
    def __init__(self, context: Match):
        super().__init__()
        self.context = context

        # Creating table of informations
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        self.robot_list = []    # stores match's robot list
        self.robot_frames = []  # stores a RobotFrame instance for each robot in match

        self.robot_list = context.robots

        for i in range(len(self.robot_list)):
            r = RobotFrame(self.robot_list[i], self.context.team_color)
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
    
    def update_info(self, context: Match):
        for robot in context.robots:
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
            robot_info = context.fetch_robot_by_id(robot.team, robot.id)
            if robot_info is not None:
                robot.update_info()

class RobotsInfo(QScrollArea):
    def __init__(self, context: Match):
        super(RobotsInfo, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#36313C'))
        self.setPalette(palette)
        self.setMinimumWidth(200)
        self.setMaximumWidth(400)

        self.robots_grid = RobotsGrid(context)

        # scroll_area = QScrollArea()
        self.setWidgetResizable(True)  # Faz com que o conteúdo se adapte ao tamanho
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setWidget(self.robots_grid)
