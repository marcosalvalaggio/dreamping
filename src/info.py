from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialog, QLabel


class Info(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Info")

        layout = QVBoxLayout()

        self.info_button = QPushButton()
        self.info_button.setText("ℹ️")
        self.info_button.setFixedWidth(20)

        layout.addWidget(self.info_button)
        self.info_button.clicked.connect(self.show_dialog)
        self.setLayout(layout)

    def show_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle("Info")
        dialog.setGeometry(100, 100, 200, 50)

        layout = QVBoxLayout()

        copyright_label = QLabel()
        copyright_label.setText("© TVS ITALIA srl - Versione: 0.1")
        layout.addWidget(copyright_label)

        dialog.setLayout(layout)

        dialog.exec_()
