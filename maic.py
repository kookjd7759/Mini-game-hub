import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Mini Game Hub")
        self.setFixedSize(300, 150) 

        layout = QVBoxLayout()

        title_lbl = QLabel("Mini Game Hub", self)
        title_lbl.setStyleSheet("font-size: 32px; font-weight: bold;")
        title_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_lbl)

        minesweeper_btn = QPushButton("Minesweeper", self)
        minesweeper_btn.setStyleSheet("font-size: 18px;")
        minesweeper_btn.clicked.connect(self.start_minesweeper)
        layout.addWidget(minesweeper_btn)

        self.setLayout(layout)

    def start_minesweeper(self):
        self.minesweeper_window = GameWindow("Minesweeper")
        self.minesweeper_window.setWindowModality(Qt.ApplicationModal)
        self.minesweeper_window.show()


class GameWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        self.initUI(title)

    def initUI(self, title):
        self.setWindowTitle(title)
        self.setFixedSize(450, 400) 

        layout = QVBoxLayout()
        label = QLabel(f"Welcome to {title}!", self)
        label.setStyleSheet("font-size: 20px; font-weight: bold;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
