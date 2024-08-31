"""
System's log displaying errors and warnings.
"""

import os
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea
from PyQt6.QtGui import QPalette, QColor, QFont
from PyQt6.QtCore import Qt

class Log(QWidget):
    def __init__(self):
        super(Log, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)

        # Access to last_session_log.txt file
        self.log_file_path = os.getcwd() + "/files/last_session_log.txt"

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Log", parent=self), alignment=Qt.AlignmentFlag.AlignTop)

        # Creating scroll area where the messages shall be displayed
        self.scroll_area = QScrollArea()
        max_w = 250
        self.scroll_area.setFixedWidth(max_w)

        # Creating widget inside scroll area to hold the messages
        self.widget = QWidget()
        self.widget.setAutoFillBackground(True)
        palette = self.widget.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#8E81A9'))
        self.widget.setPalette(palette)
        self.widget.setFixedWidth(max_w-16)

        self.vbox = QVBoxLayout()
        self.widget.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        # self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.widget)

        layout.addWidget(self.scroll_area)

        # Managing the scrollbar's height
        self.vscrollbar = self.scroll_area.verticalScrollBar()
        self.vscrollbar.rangeChanged.connect(self.scrollToBottomIfNeeded)
        self.vscrollbar.valueChanged.connect(self.storeAtBottomState)
        self.atbottom = True

        # widget stretch

        self.setLayout(layout)
    
    def add_message(self, m):
        msg = QLabel(">> " + str(m), parent=self)
        msg.setFont(QFont('Arial', 14))
        msg.setWordWrap(True)
        self.vbox.addWidget(msg, alignment=Qt.AlignmentFlag.AlignTop)
        
        # Add message to log file
        log_file = open(self.log_file_path, "a")
        log_file.write(">> " + str(m) + "\n")
        log_file.close()
    
    def storeAtBottomState(self, value):
        self.atbottom = value == self.vscrollbar.maximum()
    
    def scrollToBottomIfNeeded(self, minimum, maximum):
        if self.atbottom:
            self.vscrollbar.setValue(maximum)
