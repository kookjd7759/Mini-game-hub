import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QComboBox, QGridLayout, QStackedWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from connector import *

class Minesweeper_Window(QWidget):
    CELL_SIZE = 32

    def __init__(self):
        super().__init__()
        self.img_path = {
            'c' : os.getcwd() + '\\Mini-game-hub\\src\\minesweeper\\close.png',
            'f' : os.getcwd() + '\\Mini-game-hub\\src\\minesweeper\\flag.png',
        }
        for i in range(0, 9):
            self.img_path[f'{i}'] = os.getcwd() + f'\\Mini-game-hub\\src\\minesweeper\\Number_{i}.png'
        self.game = MINESWEEPER_EXE()
        send(self.game, '0')
        self.initUI(8, 10)

    def initUI(self, x : int, y : int):
        self.x = x
        self.y = y
        self.setWindowTitle("Minesweeper")
        self.setFixedSize(self.CELL_SIZE * y, self.CELL_SIZE * x + 26)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)

        hbox_info = QHBoxLayout()
        self.level_selcet = QComboBox(self)
        self.level_selcet.addItem('BEGINNER')
        self.level_selcet.addItem('INTERMEDIATE')
        self.level_selcet.addItem('ADVANCED')
        self.level_selcet.setFixedWidth(130)
        hbox_info.addWidget(self.level_selcet, 0, Qt.AlignLeft)
        vbox.addLayout(hbox_info)

        self.board = [[None for _ in range(y)] for _ in range(x)]
        self.board_grid = QGridLayout()
        self.board_grid.setSpacing(0)
        for i in range(x):
            for j in range(y):
                label = QLabel(self)
                label.setPixmap(QPixmap(self.img_path['c']).scaled(self.CELL_SIZE, self.CELL_SIZE, Qt.KeepAspectRatio))
                label.setFixedSize(self.CELL_SIZE, self.CELL_SIZE)
                self.board_grid.addWidget(label, i, j)
                self.board[i][j] = ['c', label]
        
        vbox.addLayout(self.board_grid)
        self.setLayout(vbox)

    def update(self):
        st = read(self.game)
        if st == "clear" or st == "lose" : 
            self.gameEnd_dialog(st)
        line = [st[i:i + self.y] for i in range(0, len(st), self.y)]
        for i in range(self.x):
            for j in range(self.y):
                if self.board[i][j][0] != line[i][j]:
                    self.board[i][j][1].deleteLater()

                    label = QLabel(self)
                    label.setPixmap(QPixmap(self.img_path[line[i][j]]).scaled(self.CELL_SIZE, self.CELL_SIZE, Qt.KeepAspectRatio))
                    label.setFixedSize(self.CELL_SIZE, self.CELL_SIZE)

                    self.board_grid.addWidget(label, i, j)

                    self.board[i][j][0] = line[i][j]
                    self.board[i][j][1] = label
        
        self.repaint()

    def mousePressEvent(self, event):
        mousePos = self.mapFromGlobal(self.mapToGlobal(event.pos()))
        y_offset = 26
        x = mousePos.x() // self.CELL_SIZE
        y = (mousePos.y() - y_offset) // self.CELL_SIZE
        print(f'{x}, {y}')
        if event.button() == Qt.LeftButton:
            send(self.game, f'{y} {x} 0')
        elif event.button() == Qt.RightButton:
            send(self.game, f'{y} {x} 1')
        self.update()
    
    def gameEnd_dialog(self, st):
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(st)
        msgBox.setInformativeText("게임을 다시 시작하시겠습니까?")
        msgBox.setWindowTitle("게임 종료")
        
        restartButton = QPushButton("재시작")
        msgBox.addButton(restartButton, QMessageBox.ActionRole)
        exitButton = msgBox.addButton(QMessageBox.Close)
        
        msgBox.exec_()

        if msgBox.clickedButton() == restartButton:
            self.restart()

    def restart(self):
        self.game = MINESWEEPER_EXE()
        send(self.game, '0')
        self.initUI(8, 10)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Minesweeper_Window()
    main_window.show()
    sys.exit(app.exec_())