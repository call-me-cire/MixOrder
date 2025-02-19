import sys

from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QProgressBar, QMainWindow, QGridLayout, QCheckBox, QVBoxLayout

from PlayListParser import PlaylistParser


def main():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MixOrder")
        self.setGeometry(100, 100, 500, 500)
        self.layout = QVBoxLayout()
        self.set_file_dialog_button()
        self.play_list_check_boxes = {}

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)
        self.parser = PlaylistParser()

    def set_file_dialog_button(self):
        file_button = QPushButton("Select file", parent = self)
        self.layout.addWidget(file_button)
        file_button.clicked.connect(self.select_file)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if not file_path:
            return
        self.parser.set_file_path(file_path)
        self.parser.get_playlists()
        self.set_playlist_check_boxes(self.parser.playListNames)


    def set_playlist_check_boxes(self, playlist_names):
        initial_height = 50
        for playlist in playlist_names:
            self.play_list_check_boxes[playlist] = (CheckBox(initial_height, playlist))

        for name, checkbox in self.play_list_check_boxes.items():
            self.layout.addWidget(checkbox)
            initial_height += 50

        sort_button = QPushButton("Sort playlists", parent = self)
        self.layout.addWidget(sort_button)

        sort_button.clicked.connect(self.sort_playlists)

    def sort_playlists(self):
        for name, checkbox in self.play_list_check_boxes.items():
            if checkbox.isChecked():
                self.parser.parse(name)

class Button(QPushButton):
    def __init__(self):
        super().__init__()
        self.move(0,400)
class CheckBox(QCheckBox):
    def __init__(self, height, label):
        super().__init__()
        self.setText(label)
        self.move(50,height)
        self.show()



main()