from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialog, QLineEdit, QDialogButtonBox, QHBoxLayout, QFileDialog
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

class SMTPConfig(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SMTP Config")
        
        self.smtp_server: str = ""
        self.smtp_port: str = ""
        self.sender_email: str = ""
        self.sender_password: str = ""
        self.reciver_email: str = ""
        self.verbose: bool = False
        self.export: bool = False
        self.imported: bool = False
        self.file_path: str = ""

        layout = QHBoxLayout()

        self.smtp_button = QPushButton()
        self.smtp_button.setText("📧")

        self.smtp_button.setFixedWidth(40)
        self.smtp_button.clicked.connect(self.show_dialog)
        layout.addWidget(self.smtp_button)

        self.setLayout(layout)

    def send_email(self, message: str = "Hello World from DreamPing") -> None:
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.reciver_email
            msg['Subject'] = 'DreamPing Status Update'
            body = f'{message}\n\n'
            msg.attach(MIMEText(body, 'plain'))
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, self.reciver_email, msg.as_string())
                server.quit()
                if self.verbose:
                    print("email send successfully")
        except Exception as e:
            if self.verbose:
                print("Error: ", e)


    def show_dialog(self) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle("SMTP Configuration")
        dialog.setGeometry(100, 100, 400, 400)
        layout = QVBoxLayout()
        
        option_layout = QHBoxLayout()
        option_layout.addStretch(1)

        self.import_button = QPushButton()
        self.import_button.setText("Import")
        self.import_button.clicked.connect(self.import_configuration)
        option_layout.addWidget(self.import_button)

        self.export_button = QPushButton()
        self.export_button.setText("Export")
        self.export_button.clicked.connect(self.export_configuration)
        option_layout.addWidget(self.export_button)

        layout.addLayout(option_layout)

        self.smtp_server_input = QLineEdit()
        self.smtp_server_input.setPlaceholderText("SMTP Server")

        self.smtp_port_input = QLineEdit()
        self.smtp_port_input.setPlaceholderText("SMTP Port (465, 587)")

        self.sender_email_input = QLineEdit()
        self.sender_email_input.setPlaceholderText("Email Mittente")
        
        self.sender_password_input = QLineEdit()
        self.sender_password_input.setEchoMode(QLineEdit.Password)
        self.sender_password_input.setPlaceholderText("Password Mittente")

        self.reciver_email_input = QLineEdit()
        self.reciver_email_input.setPlaceholderText("Email Destinatario")

        layout.addWidget(self.smtp_server_input)
        layout.addWidget(self.smtp_port_input)
        layout.addWidget(self.sender_email_input)
        layout.addWidget(self.sender_password_input)
        layout.addWidget(self.reciver_email_input)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        dialog.setLayout(layout)

        result = dialog.exec_()

        if result == QDialog.Accepted:
            self.smtp_server = self.smtp_server_input.text()
            self.smtp_port = self.smtp_port_input.text()
            self.sender_email = self.sender_email_input.text()
            self.sender_password = self.sender_password_input.text()
            self.reciver_email = self.reciver_email_input.text()
            config_data = [self.smtp_server, self.smtp_port, self.sender_email, self.sender_password, self.reciver_email]
            self.export_configuration()
            if self.verbose:
                print("Config Data:", config_data)


    def import_configuration(self) -> None:
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Import Configuration", "", "JSON Files (*.json)")
        if file_path:
            with open(file_path, "r") as file:
                config_data = json.load(file)
                try:
                    self.smtp_server = config_data.get("smtp_server", "")
                    self.smtp_port = config_data.get("smtp_port", "")
                    self.sender_email = config_data.get("sender_email", "")
                    self.sender_password = config_data.get("sender_password", "")
                    self.reciver_email = config_data.get("reciver_email", "")
                except:
                    self.smtp_server = ""
                    self.smtp_port = ""
                    self.sender_email = ""
                    self.sender_password = ""
                    self.reciver_email = ""
        
        self.smtp_server_input.setText(self.smtp_server)
        self.smtp_port_input.setText(self.smtp_port)
        self.sender_email_input.setText(self.sender_email)
        self.sender_password_input.setText(self.sender_password)
        self.reciver_email_input.setText(self.reciver_email)

        self.imported = True



    def export_configuration(self) -> None:
        if self.export == False and self.imported == False:
            file_dialog = QFileDialog()
            self.file_path, _ = file_dialog.getSaveFileName(self, "Export Configuration", "", "JSON Files (*.json)")
            self.export = True
        else:
            if self.file_path:
                try:
                    config_data = {
                        "smtp_server": self.smtp_server,
                        "smtp_port": self.smtp_port,
                        "sender_email": self.sender_email,
                        "sender_password": self.sender_password,
                        "reciver_email": self.reciver_email
                    }
                except:
                    config_data = {}
                with open(self.file_path, "w") as file:
                    json.dump(config_data, file, indent=4)
        
                