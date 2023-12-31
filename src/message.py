from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialog, QLineEdit, QDialogButtonBox, QHBoxLayout, QLabel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
        self.verbose = False

        layout = QHBoxLayout()

        self.smtp_button = QPushButton()
        self.smtp_button.setText("📧")

        # font = self.smtp_button.font()
        # font.setPointSize(12)  # Change the size to your desired value
        # self.smtp_button.setFont(font)

        self.smtp_button.setFixedWidth(40)
        self.smtp_button.clicked.connect(self.show_dialog)
        layout.addWidget(self.smtp_button)

        self.setLayout(layout)

    def send_email(self, message: str = "Hello World from DreamPing"):
        try:
            # Create the MIME object
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.reciver_email
            msg['Subject'] = 'DreamPing Status Update'
            # Add body to the email
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


    def show_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("SMTP Configuration")
        dialog.setGeometry(400, 400, 400, 400)

        layout = QVBoxLayout()

        smtp_server_input = QLineEdit()
        smtp_server_input.setPlaceholderText("Enter SMTP Server name")

        smtp_port_input = QLineEdit()
        smtp_port_input.setPlaceholderText("Enter SMTP Port number (465, 587)")

        sender_email_input = QLineEdit()
        sender_email_input.setPlaceholderText("Enter Sender Email")
        
        sender_password_input = QLineEdit()
        sender_password_input.setEchoMode(QLineEdit.Password)
        sender_password_input.setPlaceholderText("Enter Sender Password")

        reciver_email_input = QLineEdit()
        reciver_email_input.setPlaceholderText("Enter Reciver Email")

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
            self.smtp_server = smtp_server_input.text()
            self.smtp_port = smtp_port_input.text()
            self.sender_email = sender_email_input.text()
            self.sender_password = sender_password_input.text()
            self.reciver_email = reciver_email_input.text()
            config_data = [self.smtp_server, self.smtp_port, self.sender_email, self.sender_password, self.reciver_email]
            if self.verbose:
                print("Config Data:", config_data)
            # self.send_email()

                