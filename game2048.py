import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from connector import *

class Game2048_Window(QWidget):
    CELL_SIZE = 100

    def restart(self):
        self.close()
        self.__init__()
        self.show()

    def load_img(self):
        src_path = os.getcwd() + '\\Mini-game-hub\\image\\2048'
        self.icon_path  = src_path + '\\icon.png'
        self.img_path = { 
            'background' : src_path + '\\background.png',
            '0' : src_path + '\\0.png'
            }
        for i in range(1, 12):
            self.img_path[f'{2 ** i}'] = src_path + f'\\{2 ** i}.png'

    def __init__(self):
        super().__init__()
        self.load_img()
        self.game = GAME2048_EXE()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("2048")
        self.setWindowIcon(QIcon(self.icon_path))
        self.setFixedSize(450, 450 + 20)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)

        self.score_lbl = QLabel('Score : 0', self)
        self.score_lbl.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.score_lbl.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.score_lbl)

        self.background = QLabel(self)
        self.background.setPixmap(QPixmap(self.img_path['background']).scaled(450, 450))
        vbox.addWidget(self.background)

        self.board = [[None for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                block = QLabel(self.background)
                block.setPixmap(QPixmap(self.img_path['0']).scaled(100, 100, Qt.KeepAspectRatio))
                block.move(self.CELL_SIZE * i + ((i + 1) * 10), self.CELL_SIZE * j + ((j + 1) * 10))
                self.board[i][j] = ['0', block]
                block.raise_()
                block.show()
        
        self.setLayout(vbox)
        self.update()

    def update(self):
        board_info = read(self.game)
        line = board_info.split()
        line = [line[i:i + 4] for i in range(0, len(line), 4)]
        for i in range(4):
            for j in range(4):
                if self.board[i][j] != line[i][j]:
                    self.board[i][j][1].deleteLater()

                    block = QLabel(self.background)
                    block.setPixmap(QPixmap(self.img_path[line[i][j]]).scaled(100, 100, Qt.KeepAspectRatio))
                    block.move(self.CELL_SIZE * j + ((j + 1) * 10), self.CELL_SIZE * i + ((i + 1) * 10))
                    self.board[i][j][0] = line[i][j]
                    self.board[i][j][1] = block
                    block.raise_()
                    block.show()

        score_info = read(self.game)
        self.score_lbl.setText(f'Score : {score_info}')

        gameOver_info = read(self.game)
        gameOver_info = gameOver_info.rstrip('\n')
        if gameOver_info != 'continue':
            self.gameEnd_dialog()
            return
    
    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Up:
            send(self.game, '0')
        elif key == Qt.Key_Down:
            send(self.game, '1')
        elif key == Qt.Key_Left:
            send(self.game, '2')
        elif key == Qt.Key_Right:
            send(self.game, '3')

        self.update()
    
    def gameEnd_dialog(self):
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Game Over")
        msgBox.setText(self.score_lbl.text())
        
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
    main_window = Game2048_Window()
    main_window.show()
    sys.exit(app.exec_())