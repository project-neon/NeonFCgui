"""
NeonFC's general informations
"""

from PyQt6.QtWidgets import QLabel, QWidget, QGridLayout
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

from entities import match, Match

class GameInfo(QWidget):
    def __init__(self):
        super(GameInfo, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#D7C3F1'))
        self.setPalette(palette)

        # TODO create error message when no information is found (after Iron Cup)
        self.game_status = 'None'
        self.update_rate = 0

        layout = QGridLayout()
        layout.addWidget(QLabel("Informações NeonFC", parent=self), 0, 0, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Label for current status
        self.lbl_status = QLabel("Status atual:<br/>" + str(self.game_status), parent=self)
        layout.addWidget(self.lbl_status, 1, 0, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        # Label for update rate
        self.lbl_rate = QLabel("Taxa de atualização:<br/>" + str(self.update_rate), parent=self)
        layout.addWidget(self.lbl_rate, 3, 0, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        self.setLayout(layout)

    def update_info(self, status: Match):
        self.game_status = status.game_status
        self.update_rate = status.update_rate
        self.lbl_status.setText("Status atual:<br/>" + str(self.game_status))
        self.lbl_rate.setText("Taxa de atualização:<br/>" + str(self.update_rate) + "ms")
