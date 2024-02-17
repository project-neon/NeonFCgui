"""
System's log displaying errors and warnings.
"""

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPalette, QColor

class Log(QWidget):
    def __init__(self):
        super(Log, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Log", parent=self))
        layout.addWidget(QLabel("Implementação futura!", parent=self))
        
        text = QLabel("Irá mostrar mensagens de erro e avisos.", parent=self)
        text.setWordWrap(True)
        layout.addWidget(text)

        self.setLayout(layout)
