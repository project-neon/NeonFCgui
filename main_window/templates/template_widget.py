from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel,
    QHBoxLayout, QVBoxLayout
)
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import QSize, Qt

"""
This is a template widget to be used as an exemple.
"""

class TemplateWidget(QWidget):
    def __init__(self):
        super(TemplateWidget, self).__init__()

        # Set background color to this widget
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)

        # Create a label
        self.template_lbl = QLabel("Template widget: ")
        
        # Create a button
        self.template_btn = QPushButton(text="Nova janela")
        # Connect button to its function
        self.template_btn.clicked.connect(self.button_func)

        # Create a variable to hold the instance of the template window
        self.template_window = TemplateWindow()

        # Create a horizontal layout
        self.h_layout = QHBoxLayout()
        # Add label to layout
        self.h_layout.addWidget(self.template_lbl)
        # Add button to layout
        self.h_layout.addWidget(self.template_btn)
        # Add horizontal layout to this TemplateWidget
        self.setLayout(self.h_layout)

    def button_func(self):
        """
        This button's function is to open an additional window.
        """
        if self.template_window.isVisible():
            self.template_window.hide()
        else:
            self.template_window.show()

class TemplateWindow(QWidget):
    """
    Additional window.
    """
    def __init__(self):
        super().__init__()

        # Set a title for this window
        self.setWindowTitle("Template Window")

        # Set minimun sizes of the window
        self.setMinimumSize(QSize(400, 200))

        # Set background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)

        # Create a vertical layout
        self.v_layout = QVBoxLayout()

        # Add a label to v_layout
        self.v_layout.addWidget(QLabel("Label1"), alignment=Qt.AlignmentFlag.AlignHCenter)
        
        # Create a dummy button
        btn1 = QPushButton(text="Dummy button")
        # Add dummy button to v_layout
        self.v_layout.addWidget(btn1, alignment=Qt.AlignmentFlag.AlignTop)

        # Set v_layout as this TemplateWindow's layout
        self.setLayout(self.v_layout)
