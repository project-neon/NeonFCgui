"""
Section of the main window where the
pop-up menu's buttons will be displayed.
"""

from PyQt6.QtWidgets import (
    QLabel, QWidget, QPushButton, QComboBox, QLineEdit,
    QHBoxLayout, QVBoxLayout, QGridLayout
)
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

class RobotParams(object):
    def __init__(self, id=0, kp=0, ki=0, kd=0, unicontroller=None):
        self.id = str(id)
        self.kp = str(kp)
        self.ki = str(ki)
        self.kd = str(kd)
        self.unicontroller = str(unicontroller)

        self.kp_line = QLineEdit()
        self.kp_line.setText(str(self.kp))
        self.kp_line.setFixedWidth(60)

        self.ki_line = QLineEdit()
        self.ki_line.setText(str(self.ki))
        self.ki_line.setFixedWidth(60)

        self.kd_line = QLineEdit()
        self.kd_line.setText(str(self.kd))
        self.kd_line.setFixedWidth(60)

        self.unicontroller_line = QLineEdit()
        self.unicontroller_line.setText(str(self.unicontroller))
        self.unicontroller_line.setFixedWidth(120)

class Control_Params(QWidget):
    """
    Additional window to show the robot's control parameters.
    """

    def __init__(self, param_list=[]):
        super().__init__()

        self.setMaximumWidth(0) # Total width of its children
        self.setMaximumHeight(0) # Total height of its children
        self.setWindowTitle("Control Parameters")
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)

        v_layout = QVBoxLayout()
        v_layout.addWidget(QLabel("<h3> Parâmetros do controle dos robôs </h3>", parent=self), alignment=Qt.AlignmentFlag.AlignHCenter)

        # Displaying parameters in a table
        self.params_table = QGridLayout()
        # TODO adicionar divisória entre as linhas e colunas da tabela?

        # param_list = [robot1_params, robot2_params]
        # robot1_params = [id, kp, ki, kd, unicontroller]
        self.robots = []
        if param_list:
            for info in param_list:
                r = RobotParams(info[0], info[1], info[2], info[3], info[4])
                self.robots.append(r)
            # Table labels
            lbl = QLabel("Robot_id", parent=self)
            lbl.setFixedHeight(20)
            self.params_table.addWidget(lbl, 0, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
            self.params_table.addWidget(QLabel("Kp", parent=self), 0, 1, alignment=Qt.AlignmentFlag.AlignHCenter)
            self.params_table.addWidget(QLabel("Ki", parent=self), 0, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
            self.params_table.addWidget(QLabel("Kd", parent=self), 0, 3, alignment=Qt.AlignmentFlag.AlignHCenter)
            self.params_table.addWidget(QLabel("Unicontroller", parent=self), 0, 4, alignment=Qt.AlignmentFlag.AlignHCenter)
        else:
            print("No robot's control parameters found.")
            msg = QLabel("No robot's control parameters found.", parent=self)
            self.params_table.addWidget(msg, 0, 0)

        # Table values
        for i in range(len(self.robots)):
            self.params_table.addWidget(
                QLabel(str(self.robots[i].id), parent=self),
                i+1, 0, # row, column
                alignment=Qt.AlignmentFlag.AlignHCenter
            )
            self.params_table.addWidget(
                self.robots[i].kp_line,
                i+1, 1,
                alignment=Qt.AlignmentFlag.AlignHCenter
            )
            self.params_table.addWidget(
                self.robots[i].ki_line,
                i+1, 2,
                alignment=Qt.AlignmentFlag.AlignHCenter
            )
            self.params_table.addWidget(
                self.robots[i].kd_line,
                i+1, 3,
                alignment=Qt.AlignmentFlag.AlignHCenter
            )
            self.params_table.addWidget(
                self.robots[i].unicontroller_line,
                i+1, 4,
                alignment=Qt.AlignmentFlag.AlignHCenter
            )

        v_layout.addLayout(self.params_table)

        # Button to change values
        self.btn_change_params = QPushButton(text="Alterar parâmetros")
        self.btn_change_params.setFixedWidth(180)
        self.btn_change_params.setFixedHeight(30)
        self.btn_change_params.clicked.connect(self.changeParams)
        v_layout.addWidget(self.btn_change_params, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(v_layout)
    
    def changeParams(self):
        for r in self.robots:
            print("-----------------------------")
            print(
                r.id + ' ' + r.kp_line.text() + ' ' +
                r.ki_line.text() + ' ' + r.kd_line.text(),
                r.unicontroller_line.text()
            )

class Menu(QWidget):
    def __init__(self, params=[]):
        super(Menu, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)

        h_layout = QHBoxLayout()

        """
        Adding parameters window
        param_list = [robot1_params, robot2_params]
        robot1_params = [id, kp, ki, kd, unicontroller]
        """
        # self.params_window = Control_Params(
        #     [[0, 8, 8, 8, "aaa"], [1, 7, 7, 7, None], [5, 10, 10, 10, 99]]
        # )
        self.params_window = Control_Params(params)

        # Button to open parameter settings
        self.params = QPushButton(text="Parâmetros", parent=self)
        self.params.setFixedSize(160, 60)
        self.params.clicked.connect(self.toggle_params)
        h_layout.addWidget(self.params, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Coach drop-down selection
        # TODO receive coach list and create msg for empty list
        self.coach_list = ['Teste 1', 'Teste 2', 'Coach Teste 3']
        self.c_coach = self.coach_list[0]
        print(f"Current Coach: {self.c_coach}")

        v_layout = QVBoxLayout()
        v_layout.addWidget(QLabel("Coach", parent=self), alignment=Qt.AlignmentFlag.AlignHCenter)

        self.btn_coach = QComboBox()
        self.btn_coach.addItems(self.coach_list)
        self.btn_coach.activated.connect(self.current_coach)
        v_layout.addWidget(self.btn_coach, alignment=Qt.AlignmentFlag.AlignHCenter)
        h_layout.addLayout(v_layout)

        self.setLayout(h_layout)

    def current_coach(self):
        coach_name = self.btn_coach.currentText()
        print(f"Current Coach: {coach_name}")
    
    def toggle_params(self):
        if self.params_window.isVisible():
            self.params_window.hide()
        else:
            self.params_window.show()
