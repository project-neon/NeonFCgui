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
        self.grid_layout.addWidget(self.radio_option_lbl, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop) # starts at row:2, column:0, spans 1 row, spans 2 columns, is aligned at the top of the grid cell
        # Checkboxes
        self.grid_layout.addWidget(self.checkbox_lbl, 3, 0) # starts at row:3, column:0
        self.grid_layout.addWidget(self.checkbox_a, 3, 1) # starts at row:3, column:1
        self.grid_layout.addWidget(self.checkbox_b, 3, 2) # starts at row:3, column:2
        self.grid_layout.addWidget(self.checkbox_c, 3, 3) # starts at row:3, column:3
        self.grid_layout.addWidget(self.checked_boxes_lbl, 4, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop) # starts at row:4, column:0, spans 1 row, spans 2 columns, is aligned at the top of the grid cell
        # Dropdown menu (Combo box)
        self.grid_layout.addWidget(self.combobox_lbl, 5, 0) # starts at row:5, column:0
        self.grid_layout.addWidget(self.combobox_btn, 5, 1, 1, 3) # starts at row:5, column:1, spans 1 row, spans 3 columns
        self.grid_layout.addWidget(self.combobox_index_lbl, 6, 0, 1, 2) # starts at row:6, column:0, spans 1 row, spans 2 columns
        self.grid_layout.addWidget(self.combobox_text_lbl, 6, 2, 1, 2) # starts at row:6, column:2, spans 1 row, spans 2 columns

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
        self.radio_option_lbl = QLabel("Radio Option: None")
        # Create 3 radio buttons
        self.radio_btn_1 = QRadioButton("Option 1")
        self.radio_btn_2 = QRadioButton("Option 2")
        self.radio_btn_3 = QRadioButton("Option 3")
        # Connect radio buttons to their function called "radio_button"
        self.radio_btn_1.toggled.connect(lambda: self.radio_button(1))
        self.radio_btn_2.toggled.connect(lambda: self.radio_button(2))
        self.radio_btn_3.toggled.connect(lambda: self.radio_button(3))

        # Create checkbox labels and buttons
        self.checkbox_lbl = QLabel("Checkboxes: ")
        self.checked_boxes_lbl = QLabel("Boxes checked: ")
        # Create 3 checkboxes
        self.checkbox_a = QCheckBox(text="A")
        self.checkbox_b = QCheckBox(text="B")
        self.checkbox_c = QCheckBox(text="C")
        # Connect checkboxes to their function called "checkboxes"
        self.checkbox_a.stateChanged.connect(self.checkboxes)
        self.checkbox_b.stateChanged.connect(self.checkboxes)
        self.checkbox_c.stateChanged.connect(self.checkboxes)

        # Create dropdown menu (Combo box) labels and buttons
        self.combobox_lbl = QLabel("ComboBox: ")
        self.combobox_index_lbl = QLabel("ComboBox index: ")
        self.combobox_text_lbl = QLabel("ComboBox text: ")
        # Create combo box and add options to it
        self.combobox_btn = QComboBox()
        # Adding items to the combobox
        self.combobox_btn.addItems(['One', 'Two', 'Six'])
        self.combobox_btn.addItem('Seven')
        self.combobox_btn.insertItem(2, 'Three')
        self.combobox_btn.insertItems(3, ['Four', 'Five'])
        # Note: An item can be removed with removeItem(int index) and all items can be removed with clear()

        # Connect combo box to its functions
        self.combobox_btn.activated.connect(self.combobox_index)
        self.combobox_btn.currentTextChanged.connect(self.combobox_text)
        # self.combobox_btn.currentIndexChanged.connect(self.combobox_index)
        # Note: currentIndexChanged() and currentTextChanged() are always emitted regardless
        # if the change was done programmatically or by user interaction, while activated()
        # is only emitted when the change is caused by user interaction.
    
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
            self.radio_option_lbl.setText(f"Radio Option: {option}")
    
    def checkboxes(self):
        text = "Boxes checked:"
        if self.checkbox_a.isChecked():
            text = text + " A"
        if self.checkbox_b.isChecked():
            text = text + " B"
        if self.checkbox_c.isChecked():
            text = text + " C"
        self.checked_boxes_lbl.setText(text)
    
    def combobox_index(self, index):
        # This function is called every time a combobox option is selected
        text = "ComboBox index: " + str(index)
        self.combobox_index_lbl.setText(text)
        # The selected combobox option's text can be obtained as follows:
        text2 = str(self.combobox_btn.currentText())
        self.combobox_text_lbl.setText("ComboBox text: " + text2)
        print("ComboBox")
    
    def combobox_text(self, text):
        # This function is only called when the text in the combobox changes
        self.combobox_text_lbl.setText("ComboBox text: " + text)
        print(text)
        # Alternatively, the selected combobox option's text can be obtained as follows:
        # print(str(self.combobox_btn.currentText()))

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
