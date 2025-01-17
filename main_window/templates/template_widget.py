from PyQt6.QtWidgets import (
    QWidget, QLabel,
    QPushButton, QRadioButton, QCheckBox, QComboBox,
    QHBoxLayout, QVBoxLayout, QGridLayout
)
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import QSize, Qt

class TemplateWidget(QWidget):
    """
    This is a template widget inside the panel.
    It can be used as an exemple and can open a window with more examples of widgets.
    """
    def __init__(self):
        super(TemplateWidget, self).__init__()

        # Set background color to this widget
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#b3a4d3'))
        self.setPalette(palette)

        # Create a label
        self.template_lbl = QLabel("Templates: ")
        
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
    Additional window with widget exemples.
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

        # Creating the template labels and buttons for the grid_layout:
        self.populate_grid()

        # Creating template labels and colored widgets for the vertical layout
        self.populate_v_layout()

        """
        # ██╗░░░░░░█████╗░██╗░░░██╗░█████╗░██╗░░░██╗████████╗░██████╗
        # ██║░░░░░██╔══██╗╚██╗░██╔╝██╔══██╗██║░░░██║╚══██╔══╝██╔════╝
        # ██║░░░░░███████║░╚████╔╝░██║░░██║██║░░░██║░░░██║░░░╚█████╗░
        # ██║░░░░░██╔══██║░░╚██╔╝░░██║░░██║██║░░░██║░░░██║░░░░╚═══██╗
        # ███████╗██║░░██║░░░██║░░░╚█████╔╝╚██████╔╝░░░██║░░░██████╔╝
        # ╚══════╝╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░░╚═════╝░░░░╚═╝░░░╚═════╝░
        """

        # This window will have a horizontal layout with 2 sections:
        # the left section includes a grid layout with labels and buttons aligned,
        # the right section has a vertical layout with diferent colors and labels.

        # Create the horizontal layout of the window
        self.h_layout = QHBoxLayout()

        # Create grid layout
        self.grid_layout = QGridLayout()
        # Create a vertical layout
        self.v_layout = QVBoxLayout()

        # Set margins around the contents of the v_layout to distance this layout from the grid
        self.v_layout.setContentsMargins(50, 0, 0, 0) # Left margin, top margin, right margin, bottom margin
        # Note: setSpacing() is a function that adds a space between all child widgets of a layout

        # Add the labels and the buttons to the grid layout:
        # Push button
        self.grid_layout.addWidget(self.push_button_lbl, 0, 0, 1, 2) # starts at row:0, column:0, spans 1 row, spans 2 columns
        self.grid_layout.addWidget(self.push_btn, 0, 2, 1, 2) # starts at row:0, column:2, spans 1 row, spans 2 columns
        # Radio button
        self.grid_layout.addWidget(self.radio_buttons_lbl, 1, 0) # starts at row:1, column:0
        self.grid_layout.addWidget(self.radio_btn_1, 1, 1) # starts at row:1, column:1
        self.grid_layout.addWidget(self.radio_btn_2, 1, 2) # starts at row:1, column:2
        self.grid_layout.addWidget(self.radio_btn_3, 1, 3) # starts at row:1, column:3
        self.grid_layout.addWidget(self.radio_option_lbl, 2, 0, alignment=Qt.AlignmentFlag.AlignTop) # starts at row:2, column:0, aligned at the top of the grid cell
        # Checkboxes
        # TODO
        # Dropdown menu
        # TODO

        # Add label and custom widgets to the vertical layout
        self.v_layout.addWidget(self.vertical_section_lbl)
        self.v_layout.addWidget(self.custom_widget_1)
        self.v_layout.addWidget(self.custom_widget_2)

        # Add grid layout to the horizontal layout
        self.h_layout.addLayout(self.grid_layout)
        # Add vertical layout to the horizontal layout
        self.h_layout.addLayout(self.v_layout)

        # Set the horizontal layout as this window's layout
        self.setLayout(self.h_layout)
    
    """
    # ██████╗░██╗░░░██╗████████╗████████╗░█████╗░███╗░░██╗░██████╗
    # ██╔══██╗██║░░░██║╚══██╔══╝╚══██╔══╝██╔══██╗████╗░██║██╔════╝
    # ██████╦╝██║░░░██║░░░██║░░░░░░██║░░░██║░░██║██╔██╗██║╚█████╗░
    # ██╔══██╗██║░░░██║░░░██║░░░░░░██║░░░██║░░██║██║╚████║░╚═══██╗
    # ██████╦╝╚██████╔╝░░░██║░░░░░░██║░░░╚█████╔╝██║░╚███║██████╔╝
    # ╚═════╝░░╚═════╝░░░░╚═╝░░░░░░╚═╝░░░░╚════╝░╚═╝░░╚══╝╚═════╝░
    """
    
    def populate_grid(self):
        # Create label for the Push Button
        self.push_button_lbl = QLabel("Push Button: ")
        # Create a Push Button
        self.push_btn = QPushButton(text="Dummy push_button")
        # Connect this button to its function called "pushed_button"
        self.push_btn.clicked.connect(self.pushed_button)

        # Create labels for the Radio Buttons (single option buttons)
        self.radio_buttons_lbl = QLabel("Radio Buttons: ")
        self.radio_option_lbl = QLabel("Selected Option: None")
        # Create 3 radio buttons
        self.radio_btn_1 = QRadioButton("Option 1")
        self.radio_btn_2 = QRadioButton("Option 2")
        self.radio_btn_3 = QRadioButton("Option 3")
        # Connect this button to its function called "radio_button"
        self.radio_btn_1.toggled.connect(lambda: self.radio_button(1))
        self.radio_btn_2.toggled.connect(lambda: self.radio_button(2))
        self.radio_btn_3.toggled.connect(lambda: self.radio_button(3))

        # Create checkbox labels and buttons
        # TODO

        # Create dropdown menu labels and buttons
        # TODO
    
    """
    # ██████╗░██╗░░░██╗████████╗████████╗░█████╗░███╗░░██╗██╗░██████╗
    # ██╔══██╗██║░░░██║╚══██╔══╝╚══██╔══╝██╔══██╗████╗░██║╚█║██╔════╝
    # ██████╦╝██║░░░██║░░░██║░░░░░░██║░░░██║░░██║██╔██╗██║░╚╝╚█████╗░
    # ██╔══██╗██║░░░██║░░░██║░░░░░░██║░░░██║░░██║██║╚████║░░░░╚═══██╗
    # ██████╦╝╚██████╔╝░░░██║░░░░░░██║░░░╚█████╔╝██║░╚███║░░░██████╔╝
    # ╚═════╝░░╚═════╝░░░░╚═╝░░░░░░╚═╝░░░░╚════╝░╚═╝░░╚══╝░░░╚═════╝░

    # ███████╗██╗░░░██╗███╗░░██╗░█████╗░████████╗██╗░█████╗░███╗░░██╗░██████╗
    # ██╔════╝██║░░░██║████╗░██║██╔══██╗╚══██╔══╝██║██╔══██╗████╗░██║██╔════╝
    # █████╗░░██║░░░██║██╔██╗██║██║░░╚═╝░░░██║░░░██║██║░░██║██╔██╗██║╚█████╗░
    # ██╔══╝░░██║░░░██║██║╚████║██║░░██╗░░░██║░░░██║██║░░██║██║╚████║░╚═══██╗
    # ██║░░░░░╚██████╔╝██║░╚███║╚█████╔╝░░░██║░░░██║╚█████╔╝██║░╚███║██████╔╝
    # ╚═╝░░░░░░╚═════╝░╚═╝░░╚══╝░╚════╝░░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝╚═════╝░
    """
    
    def pushed_button(self):
        # This is the Push Button's function
        print(self.sender().text()) # Sender is the widget that sent the signal (in this case it's the push_button)
        self.push_button_lbl.setText("Push Button (pushed): ")
    
    def radio_button(self, option):
        if option:
            self.radio_option_lbl.setText(f"Selected Option: {option}")

    """
    # ░█████╗░██╗░░░██╗░██████╗████████╗░█████╗░███╗░░░███╗
    # ██╔══██╗██║░░░██║██╔════╝╚══██╔══╝██╔══██╗████╗░████║
    # ██║░░╚═╝██║░░░██║╚█████╗░░░░██║░░░██║░░██║██╔████╔██║
    # ██║░░██╗██║░░░██║░╚═══██╗░░░██║░░░██║░░██║██║╚██╔╝██║
    # ╚█████╔╝╚██████╔╝██████╔╝░░░██║░░░╚█████╔╝██║░╚═╝░██║
    # ░╚════╝░░╚═════╝░╚═════╝░░░░╚═╝░░░░╚════╝░╚═╝░░░░░╚═╝

    # ░██╗░░░░░░░██╗██╗██████╗░░██████╗░███████╗████████╗
    # ░██║░░██╗░░██║██║██╔══██╗██╔════╝░██╔════╝╚══██╔══╝
    # ░╚██╗████╗██╔╝██║██║░░██║██║░░██╗░█████╗░░░░░██║░░░
    # ░░████╔═████║░██║██║░░██║██║░░╚██╗██╔══╝░░░░░██║░░░
    # ░░╚██╔╝░╚██╔╝░██║██████╔╝╚██████╔╝███████╗░░░██║░░░
    # ░░░╚═╝░░░╚═╝░░╚═╝╚═════╝░░╚═════╝░╚══════╝░░░╚═╝░░░
    """

    class CustomWidget(QWidget):
        """
        This is a custom widget to be placed in this window's vertical layout.
        """
        def __init__(self, color, number):
            super().__init__()

            # Set background color
            self.setAutoFillBackground(True)
            palette = self.palette()
            palette.setColor(QPalette.ColorRole.Window, QColor(color))
            self.setPalette(palette)

            # Create a label and add it to the layout of this widget
            layout = QVBoxLayout()
            layout.addWidget(QLabel("Widget " + str(number)))
            self.setLayout(layout)

    def populate_v_layout(self):
        """
        This window's vertical layout will have 1 label and 2 custom colored widgets.
        """
        # Creating label with a diferent text font
        self.vertical_section_lbl = QLabel("Vertical layout:")

        # Create custom widget with green background
        self.custom_widget_1 = self.CustomWidget("green", 1)
        # Create custom widget with blue background
        self.custom_widget_2 = self.CustomWidget("blue", 2)
