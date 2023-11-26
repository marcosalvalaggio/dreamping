from PySide6.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem
from engine import get_mac_address, get_mac_info

class HostTable(QWidget):
    def __init__(self):
        super().__init__() 
        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("host")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("name") 
        host_button = QPushButton("+")
        host_button.setFixedWidth(30)
        remove_host_button = QPushButton("🗑️")
        remove_host_button.setFixedWidth(30)
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Host Address', 'Host Name', 'Host Status', 'Mac Address', 'Mac Info     '])

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.host_input)
        horizontal_layout.addWidget(self.name_input) 
        horizontal_layout.addWidget(host_button)
        horizontal_layout.addWidget(remove_host_button)

        layout = QVBoxLayout()
        layout.addLayout(horizontal_layout)
        layout.addWidget(self.table)

        host_button.clicked.connect(self.add_host)
        remove_host_button.clicked.connect(self.remove_host)
        
        self.setLayout(layout)

    def add_host(self) -> None:
        host_address = self.host_input.text()
        host_name = self.name_input.text()
        mac = get_mac_address(host_address)
        mac_info = get_mac_info(mac)
        if host_address and host_name:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(host_address))
            self.table.setItem(row_position, 1, QTableWidgetItem(host_name))
            self.table.setItem(row_position, 2, QTableWidgetItem("⚪"))
            self.table.setItem(row_position, 3, QTableWidgetItem(mac))
            self.table.setItem(row_position, 4, QTableWidgetItem(mac_info))
        self.host_input.clear()
        self.name_input.clear()

    def remove_host(self) -> None:
        selected_items = self.table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            self.table.removeRow(row)

