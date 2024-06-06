from PyQt6.QtWidgets import QWidget, QRadioButton, QLabel, QVBoxLayout
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt
from main_window.widgets.log import Log
import os

class CategorySelect(QWidget):
    def __init__(self):
        super(CategorySelect, self).__init__()
        self.path_to_icon = os.getcwd()+"/main_window/images/futebol.png"
        self.label = QLabel(self)
        css_text = "background-image: url('"+self.path_to_icon+"');"
        self.label.setStyleSheet(css_text)
        Layout = QVBoxLayout()
        Layout.addWidget(self.label)
        self.setLayout(Layout)


class GameMode(QWidget):
    def __init__(self, log: Log):
        super(GameMode, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)
        self.log= log

        self.mode = 'training'

        # Creating game mode 'checkboxes' (radio buttons)
        self.btn_trainning = QRadioButton(text="Modo de treino", parent=self)
        self.btn_trainning.toggled.connect(self.selectMode)
        self.btn_trainning.setFont(QFont('Arial', 15))
        self.btn_trainning.setStyleSheet("QRadioButton::font {spacing : 20px;}"
            "QRadioButton::indicator"
            "{"
            "width : 20px;"
            "height : 20px;"
            "}"
        )
        
        self.btn_competition = QRadioButton(text="Modo competição", parent=self)
        self.btn_competition.toggled.connect(self.selectMode)
        self.btn_competition.setFont(QFont('Arial', 15))
        self.btn_competition.setStyleSheet("QRadioButton::indicator"
            "{"
            "width : 20px;"
            "height : 20px;"
            "}"
        )

        self.btn_trainning.setChecked(True)

        mode_layout = QVBoxLayout()
        mode_layout.addWidget(QLabel("Modo", parent=self), alignment=Qt.AlignmentFlag.AlignHCenter)
        mode_layout.addWidget(self.btn_trainning)
        mode_layout.addWidget(self.btn_competition)
        self.setLayout(mode_layout)

    def selectMode(self):
        sender = self.sender()
        if sender.isChecked():
            if sender == self.btn_trainning:
                self.mode = 'trainning'
                self.log.add_message('Modo alterado: Treino')
            elif sender == self.btn_competition:
                self.mode = 'competition'
                self.log.add_message('Modo alterado: Competicao')
            print("Mode: "+self.mode)
