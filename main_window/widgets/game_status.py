import os
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel,
    QHBoxLayout, QSizePolicy
)
from PyQt6.QtGui import QPalette, QColor, QFont, QIcon
from PyQt6.QtCore import QSize, Qt
from entities.match import Match
from main_window.widgets.log import Log

class GameStatus(QWidget):
    def __init__(self, context: Match, log: Log, parent_panel):
        super(GameStatus, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#D7C3F1'))
        self.setPalette(palette)

        self.context = context
        self.log = log
        self.parent_panel = parent_panel

        parent_width = self.parent_panel.width()
        parent_height = self.parent_panel.height()

        # Creating the START, STOP and HALT buttons
        # To add icon to the button we will use the QIcon object, which
        # gets the path to an SVG image
        self.path_to_icons = os.getcwd()+"/main_window/images/"

        self.btn_start = QPushButton(icon=QIcon(self.path_to_icons+"start.svg"), text=" START", parent=self)
        self.btn_start.clicked.connect(self.gameStatus)

        self.btn_stop = QPushButton(icon=QIcon(self.path_to_icons+"halt.svg"), text=" STOP", parent=self)
        self.btn_stop.clicked.connect(self.gameStatus)
        
        self.btn_halt = NotImplemented
        if self.context.category == "SSL":
            self.btn_halt = QPushButton(icon=QIcon(self.path_to_icons+"reset.svg"), text=" HALT", parent=self)
            self.btn_halt.clicked.connect(self.gameStatus)

        # Adding buttons to layout
        layout = QHBoxLayout()
        # widget_label = QLabel("Estado: ")
        # widget_label.setFixedHeight(int(int(parent_height/8)/1.8))
        # layout.addWidget(widget_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(self.btn_start)
        layout.addWidget(self.btn_stop)
        if context.category == "SSL":
            layout.addWidget(self.btn_halt)
        layout.setSpacing(30)
        layout.setContentsMargins(30, 10, 30, 10)  # left, top, right, bottom

        self.setLayout(layout)

    def gameStatus(self):
        sender = self.sender()

        if sender is self.btn_start:
            self.context.set_game_status("GAME_ON")
            self.log.add_message("Status atual: GAME_ON")
        elif sender is self.btn_stop:
            self.context.set_game_status("STOP")
            self.log.add_message("Status atual: STOP")
        elif sender is self.btn_halt:
            self.context.set_game_status("HALT")
            self.log.add_message("Status atual: HALT")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_button_sizes()

    def update_button_sizes(self):
        w = self.width()
        h = self.height()
        
        icon_size = QSize(int(h/(1.8)), int(h/(1.8)))
        btn_size = QSize(int(w/10), int(h/(1.4)))
        font_size = int(h/5)

        btn_list = [self.btn_start, self.btn_stop]
        if self.context.category == "SSL":
            btn_list.append(self.btn_halt)

        for btn in btn_list:
            if btn:
                btn.setIconSize(icon_size)
                btn.setMinimumSize(btn_size)
                btn.setMaximumHeight(btn_size.height())
                btn.setFont(QFont('Arial', font_size))
                btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
