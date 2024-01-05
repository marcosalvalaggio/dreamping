from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialog, QLineEdit, QDialogButtonBox, QHBoxLayout, QLabel

class SMTPConfig(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SMTP Config")
        self.setGeometry(100, 100, 400, 100)
        
        self.smtp_server = ""
        self.smtp_port = ""
        self.sender_email = ""
        self.sender_password = ""
        self.reciver_email = ""

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
        dialog.setGeometry(400, 400, 400, 400)

        layout = QVBoxLayout()

        smtp_server_input = QLineEdit()
        smtp_server_input.setPlaceholderText("Enter SMTP Server name")
        self.smtp_server = smtp_server_input.text()

        smtp_port_input = QLineEdit()
        smtp_port_input.setPlaceholderText("Enter SMTP Port number")
        self.smtp_port = smtp_port_input.text()

        sender_email_input = QLineEdit()
        sender_email_input.setPlaceholderText("Enter Sender Email")
        self.sender_email = sender_email_input.text()
        
        sender_password_input = QLineEdit()
        sender_password_input.setPlaceholderText("Enter Sender Password")
        self.sender_password = sender_password_input.text()

        reciver_email_input = QLineEdit()
        reciver_email_input.setPlaceholderText("Enter Reciver Email")
        self.reciver_email = reciver_email_input.text()

        layout.addWidget(smtp_server_input)
        layout.addWidget(smtp_port_input)
        layout.addWidget(sender_email_input)
        layout.addWidget(sender_password_input)
        layout.addWidget(reciver_email_input)
        

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        dialog.setLayout(layout)

        result = dialog.exec_()

        if result == QDialog.Accepted:
            config_data = [self.smtp_server, self.smtp_port, self.sender_email, self.sender_password, self.reciver_email]
            # You can use the config_data as needed
            print("Config Data:", config_data)

            