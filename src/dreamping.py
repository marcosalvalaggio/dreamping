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
from engine import host_pipeline
from status import StatusLabel
from message import SMTPConfig
from info import Info
import json
import os

class DreamPingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DreamPing")
        self.setGeometry(100, 100, 400, 400)
        self.play_status: bool = False
        self.stop_status: bool = False
        self.running_status: bool = False
        self.already_running: bool = False
        self.verbose: bool = False

        central_widget = QWidget()

        layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()
        setup_horizontal_layout = QHBoxLayout()

        self.delay_widget = DelayButton()
        self.save_widget = FileSaveButton()
        self.host_widget = HostTable()
        self.mail_widget = SMTPConfig()
        play_widget = PlayButton()  
        stop_widget = StopButton()
        self.status_label = StatusLabel()
        self.export_button = QPushButton()
        self.export_button.setText("Export")
        self.export_button.setFixedWidth(60)
        self.import_button = QPushButton()
        self.import_button.setText("Import")
        self.import_button.setFixedWidth(60)
        info_widget = Info()

        setup_horizontal_layout.addWidget(info_widget)
        setup_horizontal_layout.addStretch(1)
        setup_horizontal_layout.addWidget(self.import_button)
        setup_horizontal_layout.addWidget(self.export_button)
        
        horizontal_layout.addWidget(self.delay_widget)
        horizontal_layout.addWidget(self.save_widget)
        horizontal_layout.addWidget(self.mail_widget)
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

        icon_path = self.get_icon_path()
        app_icon = QIcon(icon_path)
        self.setWindowIcon(app_icon)

    def get_icon_path(self):
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, "logo.ico")
        else:
            icon_path = "logo.ico"
        return icon_path


    def thread_play(self, delay: int, save_path: str, hosts: List[str], names: List[str]) -> None:
        self.running_status = True
        entity_status = []
        while self.running_status:
            status = host_pipeline(hosts=hosts, names=names, save_path=save_path)
            if status != entity_status:
                if self.verbose:
                    print("smtp send")
                self.mail_widget.send_email(message=str(status))
            else:
                if self.verbose:
                    print("no smtp send")
            entity_status = status
            [self.host_widget.table.setItem(idx, 2, QTableWidgetItem("🟢"  if elem[hosts[idx]] == "alive" else "🟠")) for idx, elem in enumerate(status)]
            if self.verbose:
                print(entity_status)
            time.sleep(delay)
            if self.stop_status:
                [self.host_widget.table.setItem(idx, 2, QTableWidgetItem("⚪")) for idx, elem in enumerate(status)]
                break 


    def play(self) -> None:
        self.play_status = True  
        self.stop_status = False
        self.host_widget.running_app_status = True

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
        
    def stop(self) -> None:
        if not self.play_status:
            self.status_label.update_status("No play has to be stopped")
        else:
            self.host_widget.running_app_status = False
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
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Export Configuration", "", "JSON Files (*.json)")
        try:
            with open(file_path, "w") as file:
                json.dump(entity, file, indent=4)
                self.status_label.update_status("Exporting successful")
        except Exception as e:
            print(e)
            self.status_label.update_status("Exporting failed")

    
    def importing(self) -> None:
        path = QFileDialog.getOpenFileName(self, "Select a file", "", "JSON Files (*.json)")[0]
        try:
            with open(path) as f:
                entity = json.load(f)
                self.status_label.update_status("Importing successful")
            num_rows = len(entity['hosts'])
            current_rows = self.host_widget.table.rowCount()
            if num_rows > current_rows:
                self.host_widget.table.setRowCount(num_rows)
            for row in range(self.host_widget.table.rowCount()):
                self.host_widget.table.setItem(row, 0, QTableWidgetItem(entity['hosts'][row].replace(" ", "")))
                self.host_widget.table.setItem(row, 1, QTableWidgetItem(entity['names'][row]))
                self.host_widget.table.setItem(row, 2, QTableWidgetItem("⚪"))
        except:
            self.status_label.update_status("Importing failed")


def main() -> None:
    app = QApplication(sys.argv)
    dream_app = DreamPingApp()
    dream_app.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
