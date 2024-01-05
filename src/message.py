from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialog, QLineEdit, QDialogButtonBox, QHBoxLayout

class SMTPConfig(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SMTP Config")
        self.setGeometry(100, 100, 400, 100)
        self.folder_path = None

        layout = QHBoxLayout()

        self.selected_path_button = QPushButton()
        self.selected_path_button.setText("✉")
        self.selected_path_button.setFixedWidth(40)
        self.selected_path_button.clicked.connect(self.show_dialog)
        layout.addWidget(self.selected_path_button)

        self.setLayout(layout)

    def show_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("SMTP Config Data")
        dialog.setGeometry(200, 200, 300, 100)

        layout = QVBoxLayout()

        config_textbox = QLineEdit()
        config_textbox.setPlaceholderText("Enter Config Data")
        layout.addWidget(config_textbox)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        dialog.setLayout(layout)

        result = dialog.exec_()

        if result == QDialog.Accepted:
            config_data = config_textbox.text()
            # You can use the config_data as needed
            print("Config Data:", config_data)

            