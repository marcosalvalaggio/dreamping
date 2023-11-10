from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel

class StatusLabel(QWidget):
    def __init__(self):
        super().__init__()
        self.input_field = QLabel('Status: Not Running')
        layout = QHBoxLayout()
        layout.addWidget(self.input_field)
        self.setLayout(layout)

    def update_status(self, message: str) -> None:
        self.input_field.setText(message)