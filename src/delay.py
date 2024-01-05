from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit

class DelayButton(QWidget):
    def __init__(self):
        super().__init__()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Delay in seconds")
        self.input_field.setFixedWidth(100)

        layout = QHBoxLayout()
        layout.addWidget(self.input_field)
        self.setLayout(layout)

    def get_delay(self):
        try:
            return int(self.input_field.text())
        except:
            return None

