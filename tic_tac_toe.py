import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QComboBox, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from connector import *

class TicTacToe_Window(QWidget):
    CELL_SIZE = 100
     
    def restart(self):
        self.close()
        self.__init__()
        self.show()

    def load_img(self):
        src_path = os.getcwd() + '\\Mini-game-hub\\image\\tic-tac-toe'
        self.icon_path  = src_path + '\\icon.png'
        self.img_path = { 
            'board' : src_path + '\\board.png',
            '1' : src_path + '\\O.png',
            '2' : src_path + '\\X.png'
            }

    def __init__(self):
        super().__init__()
        self.load_img()
        self.game = TICTACTOE_EXE()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Tic Tac Toe")
        self.setWindowIcon(QIcon(self.icon_path))
        self.setFixedSize(self.CELL_SIZE * 3, self.CELL_SIZE * 3 + 20)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)

        self.turn_lbl = QLabel('O\'s turn', self)
        self.turn_lbl.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.turn_lbl.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.turn_lbl)

        self.background = QLabel(self)
        self.background.setPixmap(QPixmap(self.img_path['board']).scaled(self.CELL_SIZE * 3, self.CELL_SIZE * 3))
        vbox.addWidget(self.background)

        self.board = [['0' for _ in range(3)] for _ in range(3)]

        self.setLayout(vbox)

    def update(self):
        board_info = read(self.game)
        print(board_info[0])
        self.turn_lbl.setText(f'{"O" if board_info[0] == "1" else "X"}\'s turn')
        board_info = board_info[1:]
        line = [board_info[i:i + 3] for i in range(0, len(board_info), 3)]
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != line[i][j]:
                    sign = QLabel(self.background)
                    sign.setPixmap(QPixmap(self.img_path[line[i][j]]).scaled(60, 60, Qt.KeepAspectRatio))
                    sign.move(self.CELL_SIZE * j + 20, self.CELL_SIZE * i + 20)
                    sign.raise_()
                    sign.show()

        gameOver_info = read(self.game)
        gameOver_info = gameOver_info.rstrip('\n')
        if gameOver_info != 'continue':
            self.gameEnd_dialog(gameOver_info)
            return
        
        
    def mousePressEvent(self, event):
        mousePos = self.mapFromGlobal(self.mapToGlobal(event.pos()))
        x = mousePos.x() // self.CELL_SIZE
        y = (mousePos.y() - 20) // self.CELL_SIZE
        send(self.game, f'{y} {x}')
        self.update()
    
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
    main_window = TicTacToe_Window()
    main_window.show()
    sys.exit(app.exec_())