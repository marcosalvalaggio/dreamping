import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QTableWidgetItem, QPushButton, QFileDialog
from PySide6.QtCore import Qt
import threading
import time 
from typing import List
from delay import DelayButton
from save_path import FileSaveButton
from host_table import HostTable
from play import PlayButton
from stop import StopButton
from log import LogCheckBox
from engine import host_pipeline
from status import StatusLabel
import pandas as pd

class DreamPingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DreamPing")
        self.setGeometry(100, 100, 500, 400)
        self.play_status = False
        self.stop_status = False
        self.running_status = False
        self.already_running = False

        central_widget = QWidget()

        layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()
        setup_horizontal_layout = QHBoxLayout()

        self.delay_widget = DelayButton()
        self.save_widget = FileSaveButton()
        self.host_widget = HostTable()
        play_widget = PlayButton()  
        stop_widget = StopButton()
        self.log_widget = LogCheckBox()
        self.status_label = StatusLabel()
        self.export_button = QPushButton()
        self.export_button.setText("Export")
        self.export_button.setFixedWidth(60)
        self.import_button = QPushButton()
        self.import_button.setText("Import")
        self.import_button.setFixedWidth(60)

        setup_horizontal_layout.addStretch(1)
        setup_horizontal_layout.addWidget(self.import_button)
        setup_horizontal_layout.addWidget(self.export_button)
        
        horizontal_layout.addWidget(self.delay_widget)
        horizontal_layout.addWidget(self.save_widget)
        horizontal_layout.addWidget(self.log_widget)
        horizontal_layout.addWidget(play_widget)
        horizontal_layout.addWidget(stop_widget)

        layout.addLayout(setup_horizontal_layout)
        layout.addWidget(self.host_widget)
        layout.addLayout(horizontal_layout)
        layout.addWidget(self.status_label)  # Added status label

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        play_widget.input_field.clicked.connect(self.play)
        stop_widget.input_field.clicked.connect(self.stop)
        self.export_button.clicked.connect(self.exporting)
        self.import_button.clicked.connect(self.importing)

    def thread_play(self, delay: int, save_path: str, hosts: List[str], names: List[str], log: bool):
        self.running_status = True
        while self.running_status:
            status = host_pipeline(hosts=hosts, names=names, save_path=save_path, log=log)
            [self.host_widget.table.setItem(idx, 2, QTableWidgetItem("🟢"  if elem[hosts[idx]] == "alive" else "🟠")) for idx, elem in enumerate(status)]
            #print(status)
            time.sleep(delay)
            if self.stop_status:
                [self.host_widget.table.setItem(idx, 2, QTableWidgetItem("⚪")) for idx, elem in enumerate(status)]
                break 

    def play(self):
        self.play_status = True  
        self.stop_status = False
        delay = self.delay_widget.get_delay()
        save_path = self.save_widget.folder_path
        log = self.log_widget.input_field.isChecked()

        if delay is None:
            self.status_label.update_status("No delay has been set")
        else:
            self.status_label.update_status(f"Running with delay {delay} seconds")
            hosts = []
            names = []
            for row in range(self.host_widget.table.rowCount()):
                host = self.host_widget.table.item(row, 0).text()
                hosts.append(host)
                name = self.host_widget.table.item(row, 1).text()
                names.append(name)
            if save_path:
                if len(hosts) != 0:
                    if not self.already_running:
                        self.already_running = True
                        self.stop_status = False
                        self.play_thread = threading.Thread(target=self.thread_play, args=(delay, save_path, hosts, names, log))
                        self.play_thread.start()
                    else:
                        self.status_label.update_status("A play is already running")
                else:
                    self.status_label.update_status("No host has been set")
            else:
                self.status_label.update_status("No path has been set")
                    
    def stop(self):
        if not self.play_status:
            self.status_label.update_status("No play has to be stopped")
        else:
            self.status_label.update_status("Not Running")
            self.play_status = False
            self.stop_status = True
            self.running_status = False
            self.already_running = False 
            self.play_thread.join()

    def exporting(self) -> None:
        entity = {
            'hosts': [],
            'names': []
        }
        for row in range(self.host_widget.table.rowCount()):
            entity['hosts'].append(self.host_widget.table.item(row, 0).text())
            entity['names'].append(self.host_widget.table.item(row, 1).text())
        df = pd.DataFrame(entity)
        path = QFileDialog.getExistingDirectory(self, "Select a Folder")
        try:
            df.to_csv(f"{path}/export.csv", index=False, sep=";")
            self.status_label.update_status("Exported host list")
        except:
            self.status_label.update_status("Exporting failed")

    def importing(self):
        path = QFileDialog.getOpenFileName(self, "Select a file", "", "CSV Files (*.csv)")[0]
        df = pd.read_csv(path, sep=";")
        num_rows, _ = df.shape
        current_rows = self.host_widget.table.rowCount()
        if num_rows > current_rows:
            self.host_widget.table.setRowCount(num_rows)
        for row in range(self.host_widget.table.rowCount()):
            self.host_widget.table.setItem(row, 0, QTableWidgetItem(df.iloc[row,0]))
            self.host_widget.table.setItem(row, 1, QTableWidgetItem(df.iloc[row, 1]))

def main():
    app = QApplication(sys.argv)
    dream_app = DreamPingApp()
    dream_app.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
