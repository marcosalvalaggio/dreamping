from PySide6.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem

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
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Host Address', 'Host Name', 'Host Status'])

        self.running_app_status: bool = False

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
        if self.running_app_status == False:
            host_address = self.host_input.text()
            host_address = host_address.replace(" ", "")
            host_name = self.name_input.text()
            if host_address and host_name:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(host_address))
                self.table.setItem(row_position, 1, QTableWidgetItem(host_name))
                self.table.setItem(row_position, 2, QTableWidgetItem("⚪"))
            self.host_input.clear()
            self.name_input.clear()
        else:
            pass

    def remove_host(self) -> None:
        if self.running_app_status == False:
            selected_items = self.table.selectedItems()
            if selected_items:
                row = selected_items[0].row()
                self.table.removeRow(row)
        else:
            pass

