from PySide6.QtWidgets import QWidget, QHBoxLayout, QCheckBox

class LogCheckBox(QWidget):
    def __init__(self):
        super().__init__()
        self.input_field = QCheckBox()
        self.input_field.setText("Log")
        layout = QHBoxLayout()
        layout.addWidget(self.input_field)
        self.setLayout(layout)

