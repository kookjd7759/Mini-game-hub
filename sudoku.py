import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QComboBox, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from connector import *

class Minesweeper_Window(QWidget):
    CELL_SIZE = 32

    def closeEvent(self, event):
        if self.game:
            self.game.terminate()
            self.game.wait()
        event.accept()

    def load_img(self):
        src_path = os.getcwd() + '\\Mini-game-hub\\image\\sudoku'
        self.icon_path  = src_path + '\\icon.png'
        self.img_path = { 
            'bg' : src_path + '\\background.png',
            '0' : src_path + '\\0.png'
            }
        for i in range(1, 9):
            self.img_path[f'{i}'] = src_path + f'\\{i}_black.png'
            self.img_path[f'{i}'] = src_path + f'\\{i}_red.png'
            self.img_path[f'{i}'] = src_path + f'\\{i}_blue.png'

    def restart(self):
        self.close()
        self.__init__()
        self.show()

    def __init__(self):
        super().__init__()
        self.load_img()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sudoku")
        self.setWindowIcon(QIcon(self.icon_path))
        self.setFixedSize(308, 308 + 29)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)

        self.restart_btn = QPushButton('Restart')
        self.restart_btn.clicked.connect(self.restart)
        vbox.addWidget(self.restart_btn)

        self.background = QLabel(self)
        self.background.setPixmap(QPixmap(self.img_path['bg']).scaled(308, 308))
        vbox.addWidget(self.background)
        
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                block = QLabel(self.background)
                block.setPixmap(QPixmap(self.img_path['0']).scaled(self.CELL_SIZE, self.CELL_SIZE, Qt.KeepAspectRatio))
                block.move(self.CELL_SIZE * i + ((i + 1) * 2), self.CELL_SIZE * j + ((j + 1) * 2))
                self.board[i][j] = ['0', block]
                block.raise_()
                block.show()
        
        self.setLayout(vbox)

    def update(self):
        board_info = read(self.game)
        line = [board_info[i:i + self.y] for i in range(0, len(board_info), self.y)]
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

        gameOver_info = read(self.game).rstrip('\n')
        if gameOver_info != 'continue':
            self.gameEnd_dialog(gameOver_info)
        

    def mousePressEvent(self, event):
        mousePos = self.mapFromGlobal(self.mapToGlobal(event.pos()))
        x = mousePos.x() // (self.CELL_SIZE + 2)
        y = (mousePos.y() - 29) // (self.CELL_SIZE + 2)
        print(f'{x}, {y}')
    
    def gameEnd_dialog(self, st):
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Game Over")
        msgBox.setText(st)
        
        restartButton = QPushButton("Restart")
        msgBox.addButton(restartButton, QMessageBox.ActionRole)
        exitButton = msgBox.addButton(QMessageBox.Close)
        
        msgBox.exec_()

        if msgBox.clickedButton() == restartButton:
            self.restart()
        elif msgBox.clickedButton() == exitButton:
            self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Minesweeper_Window()
    main_window.show()
    sys.exit(app.exec_())