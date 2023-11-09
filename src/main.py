import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QLabel  # Added QLabel
import asyncio
import threading
from typing import List

from delay import DelayButton
from save_path import FileSaveButton
from host_table import HostTable
from play import PlayButton
from stop import StopButton
from log import LogCheckBox
from engine import host_pipeline

class DreamPingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DreamPing")
        self.setGeometry(100, 100, 500, 400)
        self.play_status = False
        self.stop_status = False
        self.running_status = False

        central_widget = QWidget()

        layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()

        self.delay_widget = DelayButton()
        self.save_widget = FileSaveButton()
        self.host_widget = HostTable()
        play_widget = PlayButton()  
        stop_widget = StopButton()
        self.log_widget = LogCheckBox()

        # Added QLabel for status
        self.status_label = QLabel('Status: Not Running')
        
        horizontal_layout.addWidget(self.delay_widget)
        horizontal_layout.addWidget(self.save_widget)
        horizontal_layout.addWidget(self.log_widget)
        horizontal_layout.addWidget(play_widget)
        horizontal_layout.addWidget(stop_widget)

        layout.addWidget(self.host_widget)
        layout.addLayout(horizontal_layout)
        layout.addWidget(self.status_label)  # Added status label

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        play_widget.input_field.clicked.connect(self.play)
        stop_widget.input_field.clicked.connect(self.stop)

    async def thread_play(self, delay: int, save_path: str, hosts: List[str], names: List[str], log: bool):
        self.running_status = True
        while self.running_status:
            await host_pipeline(hosts=hosts, names=names, save_path=save_path, log=log)
            await asyncio.sleep(delay)
            if self.stop_status:
                break 

    def play(self):
        self.play_status = True  
        self.stop_status = False
        delay = self.delay_widget.get_delay()
        save_path = self.save_widget.folder_path
        log = self.log_widget.input_field.isChecked()

        if delay is None:
            self.update_status("No delay has been set")
        else:
            self.update_status(f"Status: Running with delay {delay} seconds")
            hosts = []
            names = []
            for row in range(self.host_widget.table.rowCount()):
                host = self.host_widget.table.item(row, 0).text()
                hosts.append(host)
                name = self.host_widget.table.item(row, 1).text()
                names.append(name)
            if save_path:
                if len(hosts) != 0:
                    self.stop_status = False
                    play_thread = threading.Thread(target=lambda: asyncio.run(self.thread_play(delay, save_path, hosts, names, log=log)))
                    play_thread.start()
                else:
                    self.update_status("No host has been set")
            else:
                self.update_status("No path has been set")
                    
    def stop(self):
        if not self.play_status:
            self.update_status("No play has to be stopped")
        else:
            self.update_status("Status: Not Running")
            self.play_status = False
            self.stop_status = True
            self.running_status = False

    def update_status(self, message):
        self.status_label.setText(message)


def main():
    app = QApplication(sys.argv)
    dream_app = DreamPingApp()
    dream_app.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
