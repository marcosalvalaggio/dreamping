import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout
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

# teoricamente sulla riga sotto posso mettere i delay in secondi e aggiungere la directory dove salvare i file del ping creando un layout QHBoxLayout
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
        
        horizontal_layout.addWidget(self.delay_widget)
        horizontal_layout.addWidget(self.save_widget)
        horizontal_layout.addWidget(self.log_widget)
        horizontal_layout.addWidget(play_widget)
        horizontal_layout.addWidget(stop_widget)

        layout.addWidget(self.host_widget)
        layout.addLayout(horizontal_layout)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Lab
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
            print("No delay has been set")
        else:
            print(delay, type(delay)) 
            print(save_path, type(save_path))
            print("Play from function") 
            hosts = []
            names = []
            for row in range(self.host_widget.table.rowCount()):
                host = self.host_widget.table.item(row, 0).text()
                hosts.append(host)
                name = self.host_widget.table.item(row, 1).text()
                names.append(name)
            print(names)
            print(hosts)
            if save_path:
                self.stop_status = False
                play_thread = threading.Thread(target=lambda: asyncio.run(self.thread_play(delay, save_path, hosts, names, log=log)))
                play_thread.start()
                    
    def stop(self):
        if not self.play_status:
            print("No play has to be stopped")
        else:
            self.play_status = False
            self.stop_status = True
            self.running_status = False
            print("Stop from function")


def main():
    app = QApplication(sys.argv)
    dream_app = DreamPingApp()
    dream_app.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
