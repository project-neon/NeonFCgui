"""
NeonFC's general informations
"""

from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

class GameInfo(QWidget):
    def __init__(self):
        super(GameInfo, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)

        # TODO how to get the info
        # TODO create error message when no information is found (after Iron Cup)
        self.game_status = 'None'
        self.update_rate = 0

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Informações NeonFC", parent=self), alignment=Qt.AlignmentFlag.AlignHCenter)

        # Label for current status
        self.lbl_status = QLabel("Status atual:<br/>" + str(self.game_status), parent=self)
        layout.addWidget(self.lbl_status, alignment=Qt.AlignmentFlag.AlignLeft)
        # TODO atualizar o texto dessa label
        # Talvez se possa criar um método que faz:
        # self.lbl_status.setText(novo_status)

        # Label for update rate
        self.lbl_rate = QLabel("Taxa de atualização:<br/>" + str(self.update_rate), parent=self)
        layout.addWidget(self.lbl_rate, alignment=Qt.AlignmentFlag.AlignLeft)
        # TODO atualizar o texto dessa label

        self.setLayout(layout)
