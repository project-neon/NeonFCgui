from PyQt6.QtWidgets import QWidget, QRadioButton, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QComboBox
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt
from entities.match import Match
from main_window.widgets.log import Log
import os

class CategorySelect(QWidget):
    def __init__(self, parent_stacked_widget):
        super(CategorySelect, self).__init__()
        self.parent_stacked_widget = parent_stacked_widget

        self.setFixedSize(1000,800)
        self.path_to_icon = os.getcwd()+"/main_window/images/futebol.png"
        self.label = QLabel(self)
        css_text = "background-image: url('"+self.path_to_icon+"');"
        self.label.setStyleSheet(css_text)

        # Creating SSL Button
        self.btn_ssl = QPushButton("SSL",self.label)
        self.btn_ssl.setStyleSheet('QPushButton {background: #FFFFFF}')
        self.btn_ssl.setGeometry(int((self.width()-200)/2), int((self.height()-80)/2)-50 , 200, 80)
        self.btn_ssl.setFont(QFont('Arial', 25))
        self.btn_ssl.clicked.connect(self.select)

        # Creating "Mini" Button
        self.btn_mini = QPushButton("MINI",self.label)
        self.btn_mini.setStyleSheet('QPushButton {background: #FFFFFF}')
        self.btn_mini.setGeometry(int((self.width()-200)/2), int((self.height()-80)/2)+50 , 200, 80)
        self.btn_mini.setFont(QFont('Arial', 25))
        self.btn_mini.clicked.connect(self.select)

        Layout = QVBoxLayout()
        Layout.addWidget(self.label)
        self.setLayout(Layout)

    def select(self):    
        sender = self.sender()
        self.parent_stacked_widget.run_category_widget(sender.text())


class GameMode(QWidget):
    def __init__(self, context: Match, log: Log):
        super(GameMode, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)
        self.context = context
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
                self.log.add_message('Modo da GUI selecionado: Treino')
            elif sender == self.btn_competition:
                self.mode = 'competition'
                self.log.add_message('Modo da GUI selecionado: Competicao')
            self.context.set_gui_mode(self.mode)
            print("Mode: "+self.mode)
    
class GoalkeeperID(QWidget):
    def __init__(self, context: Match, log: Log):
        super(GoalkeeperID, self).__init__()
        self.context = context
        self.log = log

        self.setAutoFillBackground(True)
        gk_palette = self.palette()
        gk_palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(gk_palette)
        # TODO format this widget
        gk_layout = QHBoxLayout()
        lbl_gk = QLabel("Goalkeeper ID: ", parent=self)
        gk_layout.addWidget(lbl_gk)
        # Update goalkeeper ID
        self.gk_id = self.context.gk_id
        self.lbl_current_gk = QLabel(str(self.gk_id), parent=self)
        gk_layout.addWidget(self.lbl_current_gk)
        # Goalkeeper ID selection
        self.btn_gk = QComboBox()
        self.btn_gk.setFixedHeight(28)
        self.btn_gk.setFixedWidth(70)
        # self.btn_gk.setSizePolicy(QSizePolicy.horizontalStretch)
        self.robots_ids_str = []
        for r_id in self.context.robots_ids:
            self.robots_ids_str.append(str(r_id))
        print(self.robots_ids_str)
        self.btn_gk.addItems(self.robots_ids_str)
        # select current gk
        # self.btn_gk.setCurrentIndex(r_index)
        self.btn_gk.activated.connect(self.select_gk)
        gk_layout.addWidget(self.btn_gk) # , alignment=Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(gk_layout)
    
    def select_gk(self):
        id_str = self.btn_gk.currentText()
        self.context.set_gk_id(int(id_str))
    
    def update_info(self, status: Match):
        self.gk_id = status.gk_id
        self.lbl_current_gk.setText(str(self.gk_id))
