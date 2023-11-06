from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton

class StopButton(QWidget):
    def __init__(self):
        super().__init__()
        self.input_field = QPushButton()
        self.input_field.setText("🛑")
        self.input_field.setFixedWidth(30)
        layout = QHBoxLayout()
        layout.addWidget(self.input_field)
        self.setLayout(layout)


