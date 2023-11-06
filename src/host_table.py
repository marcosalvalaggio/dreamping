from PySide6.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QPushButton, QVBoxLayout

class HostTable(QWidget):
    def __init__(self):
        super().__init__() 
        host_input = QLineEdit()
        host_input.setPlaceholderText("host")
        name_input = QLineEdit()
        name_input.setPlaceholderText("name") 
        host_button = QPushButton("+")
        host_button.setFixedWidth(30)
        remove_host_button = QPushButton("🗑️")
        remove_host_button.setFixedWidth(30)


        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(host_input)
        horizontal_layout.addWidget(name_input) 
        horizontal_layout.addWidget(host_button)
        horizontal_layout.addWidget(remove_host_button)

        layout = QVBoxLayout()
        layout.addLayout(horizontal_layout)

        self.setLayout(layout)