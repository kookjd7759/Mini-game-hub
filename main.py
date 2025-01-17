import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

from minesweeper import *
from tic_tac_toe import *

image_path = os.getcwd() + '\\Mini-game-hub\\image'
icon_path  = image_path + '\\main_icon.png'
gameList = [
    (image_path + "\\minesweeper\\icon.png", "Minesweeper"),
    (image_path + "\\tic-tac-toe\\icon.png", "Tic Tac Toe")
]

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Mini Game Hub")
        self.setWindowIcon(QIcon(icon_path))
        self.setFixedSize(300, 150) 

        layout = QVBoxLayout()

        title_lbl = QLabel("Mini Game Hub", self)
        title_lbl.setStyleSheet("font-size: 32px; font-weight: bold;")
        title_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_lbl)

        for i in range(len(gameList)):
            self.make_btn(layout, i)

        self.setLayout(layout)
        self.grab().save(f'{image_path}\\execution screen\\main.png', 'PNG') # auto Screenshot for project introduction

    def make_btn(self, layout, idx):
        icon = QIcon(QPixmap(gameList[idx][0]))
        text = gameList[idx][1]
        btn = QPushButton(f' {text}', self)
        btn.setIcon(icon)
        btn.setIconSize(icon.pixmap(30, 30).size())
        btn.setStyleSheet("font-size: 18px;")
        btn.clicked.connect(lambda: self.start_game(idx))
        layout.addWidget(btn)

    def start_game(self, idx):
        self.game_window = None
        if idx == 0:
            self.game_window = Minesweeper_Window()
        elif idx == 1:
            self.game_window = TicTacToe_Window()

        self.game_window.setWindowModality(Qt.ApplicationModal)
        self.game_window.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
