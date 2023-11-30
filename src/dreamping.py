import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QTableWidgetItem, QPushButton, QFileDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
import threading
import time 
from typing import List
from delay import DelayButton
from save_path import FileSaveButton
from host_table import HostTable
from play import PlayButton
from stop import StopButton
from engine import host_pipeline, get_mac_address, get_mac_info
from status import StatusLabel
import pandas as pd


class DreamPingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DreamPing")
        self.setGeometry(100, 100, 600, 400)
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
        horizontal_layout.addWidget(play_widget)
        horizontal_layout.addWidget(stop_widget)
        horizontal_layout.addStretch(1)

        layout.addLayout(setup_horizontal_layout)
        layout.addWidget(self.host_widget)
        layout.addLayout(horizontal_layout)
        layout.addWidget(self.status_label)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        play_widget.input_field.clicked.connect(self.play)
        stop_widget.input_field.clicked.connect(self.stop)
        self.export_button.clicked.connect(self.exporting)
        self.import_button.clicked.connect(self.importing)

    def thread_play(self, delay: int, save_path: str, hosts: List[str], names: List[str]):
        self.running_status = True
        entity_status = []
        while self.running_status:
            status = host_pipeline(hosts=hosts, names=names, save_path=save_path)
            if status != entity_status:
                print("smtp send")
            else:
                print("no smtp send")
            entity_status = status
            [self.host_widget.table.setItem(idx, 2, QTableWidgetItem("🟢"  if elem[hosts[idx]] == "alive" else "🟠")) for idx, elem in enumerate(status)]
            print(entity_status)
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
            if len(hosts) != 0:
                if not self.already_running:
                    self.already_running = True
                    self.stop_status = False
                    self.play_thread = threading.Thread(target=self.thread_play, args=(delay, save_path, hosts, names))
                    self.play_thread.start()
                else:
                    self.status_label.update_status("A play is already running")
        
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
        try:
            df = pd.read_csv(path, sep=";")
            num_rows, _ = df.shape
            current_rows = self.host_widget.table.rowCount()
            if num_rows > current_rows:
                self.host_widget.table.setRowCount(num_rows)
            for row in range(self.host_widget.table.rowCount()):
                mac = get_mac_address(df.iloc[row,0])
                mac_info = get_mac_info(mac)
                self.host_widget.table.setItem(row, 0, QTableWidgetItem(df.iloc[row,0]))
                self.host_widget.table.setItem(row, 1, QTableWidgetItem(df.iloc[row, 1]))
                self.host_widget.table.setItem(row, 2, QTableWidgetItem("⚪"))
                self.host_widget.table.setItem(row, 3, QTableWidgetItem(mac)) 
                self.host_widget.table.setItem(row, 4, QTableWidgetItem(mac_info)) 
        except:
            self.status_label.update_status("Importing failed")

def main():
    app = QApplication(sys.argv)
    app_icon = QIcon("../logo.ico")
    app.setWindowIcon(app_icon)
    dream_app = DreamPingApp()
    dream_app.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
