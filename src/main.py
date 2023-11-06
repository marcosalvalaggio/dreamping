import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout

from delay import DelayButton
from save_path import FileSaveButton
from host_table import HostTable

# teoricamente sulla riga sotto posso mettere i delay in secondi e aggiungere la directory dove salvare i file del ping creando un layout QHBoxLayout
class DreamPingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DreamPing")
        self.setGeometry(100, 100, 500, 400)

        central_widget = QWidget()

        layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()

        delay_widget = DelayButton()
        save_widget = FileSaveButton()
        host_widget = HostTable()
        
        horizontal_layout.addWidget(delay_widget)
        horizontal_layout.addWidget(save_widget)

        layout.addWidget(host_widget)
        layout.addLayout(horizontal_layout)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        print(delay_widget.get_delay())


def main():
    app = QApplication(sys.argv)
    dream_app = DreamPingApp()
    dream_app.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
