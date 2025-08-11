from PyQt6.QtWidgets import QWidget, QRadioButton, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QComboBox
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt
from entities.match import Match
from main_window.widgets.log import Log
import os

class GUIMode(QWidget):
    def __init__(self, context: Match, log: Log):
        super(GUIMode, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#D7C3F1'))
        self.setPalette(palette)
        self.context = context
        self.log= log

        self.mode = 'training'

        # Creating game mode 'checkboxes' (radio buttons)
        self.btn_trainning = QRadioButton(text="Modo de treino", parent=self)
        self.btn_trainning.toggled.connect(self.selectMode)
        self.btn_trainning.setFont(QFont('Arial', 14))
        self.btn_trainning.setStyleSheet("QRadioButton::font {spacing : 20px;}"
            "QRadioButton::indicator"
            "{"
            "width : 20px;"
            "height : 20px;"
            "}"
        )
        
        self.btn_competition = QRadioButton(text="Modo competição", parent=self)
        self.btn_competition.toggled.connect(self.selectMode)
        self.btn_competition.setFont(QFont('Arial', 14))
        self.btn_competition.setStyleSheet("QRadioButton::indicator"
            "{"
            "width : 20px;"
            "height : 20px;"
            "}"
        )

        self.btn_trainning.setChecked(True)

        mode_layout = QVBoxLayout()
        mode_layout.addWidget(QLabel("Modo da interface", parent=self), alignment=Qt.AlignmentFlag.AlignHCenter)
        mode_layout.addWidget(self.btn_trainning)
        mode_layout.addWidget(self.btn_competition)
        self.setLayout(mode_layout)

    def selectMode(self):
        sender = self.sender()
        if sender.isChecked():
            if sender == self.btn_trainning:
                self.mode = 'trainning'
                self.log.add_message('Modo da GUI selecionado: Treino')
            elif sender == self.btn_competition:
                self.mode = 'competition'
                self.log.add_message('Modo da GUI selecionado: Competicao')
            self.context.set_gui_mode(self.mode)
            print("Mode: "+self.mode)
