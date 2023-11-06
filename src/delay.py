from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit

class DelayButton(QWidget):
    def __init__(self):
        super().__init__()
        input_field = QLineEdit()
        input_field.setPlaceholderText("Delay in seconds")
        layout = QHBoxLayout()
        layout.addWidget(input_field)
        self.setLayout(layout)
