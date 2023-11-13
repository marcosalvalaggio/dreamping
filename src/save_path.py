from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QFileDialog

class FileSaveButton(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select a Path for File Storage")
        self.setGeometry(100, 100, 400, 100)
        self.folder_path = None

        layout = QHBoxLayout()

        self.selected_path_button = QPushButton()
        self.selected_path_button.setText("Select Path")
        self.selected_path_button.setFixedWidth(80)
        self.selected_path_button.clicked.connect(self.show_dialog)
        layout.addWidget(self.selected_path_button)

        self.setLayout(layout)

    def show_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select a Folder")
        if folder_path:
            folder_path_to_print = str(folder_path.replace("C:/", "").split("/")[-1])
            folder_path_to_print = f"../{folder_path_to_print}"
            #print(folder_path)
            self.folder_path = folder_path
            self.selected_path_button.setText(folder_path_to_print)

            