import sys
import os
import time

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QComboBox, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from connector import *

class Memory_Window(QWidget):
    isPlaying = False

    def restart(self):
        self.close()
        self.__init__()
        self.show()

    def load_img(self):
        src_path = os.getcwd() + '\\Mini-game-hub\\image\\memory'
        self.icon_path  = src_path + '\\icon.png'
        self.img_path = { 'bg' : src_path + '\\background.png' }
        for i in range(0, 3):
            self.img_path[f'{i}'] = src_path + f'\\{i}.png'

    def __init__(self):
        super().__init__()
        self.load_img()
        self.game = MEMORY_EXE()
        self.initUI()

    def delete_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.board[i][j][1].deleteLater()

    def create_board(self):
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        cell_size = int((420 - (self.board_size + 1) * 2) / self.board_size)
        for i in range(self.board_size):
            for j in range(self.board_size):
                block = QLabel(self.background)
                block.setPixmap(QPixmap(self.img_path['0']).scaled(cell_size, cell_size, Qt.KeepAspectRatio))
                block.move(cell_size * i + ((i + 1) * 2), cell_size * j + ((j + 1) * 2))
                self.board[i][j] = ['0', block]
                block.raise_()
                block.show()

    def initUI(self):
        self.setWindowTitle("Memory")
        self.setWindowIcon(QIcon(self.icon_path))
        self.setFixedSize(420, 420 + 29)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)

        hbox = QHBoxLayout()
        self.score_lbl = QLabel('Score : 0', self)
        self.score_lbl.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.score_lbl.setAlignment(Qt.AlignCenter)
        hbox.addWidget(self.score_lbl)

        self.start_btn = QPushButton('Start')
        self.start_btn.clicked.connect(self.start)
        hbox.addWidget(self.start_btn)

        vbox.addLayout(hbox)

        self.background = QLabel(self)
        self.background.setPixmap(QPixmap(self.img_path['bg']).scaled(420, 420))
        vbox.addWidget(self.background)

        self.board_size = 3
        self.create_board()

        self.setLayout(vbox)

    def showOnes(self):
        data = read(self.game)
        tempList = []
        cell_size = int((420 - (self.board_size + 1) * 2) / self.board_size)
        line = [data[i:i + self.board_size] for i in range(0, len(data), self.board_size)]
        for i in range(self.board_size):
            for j in range(self.board_size):
                if line[i][j] == '1':
                    label = QLabel(self.background)
                    label.setPixmap(QPixmap(self.img_path[line[i][j]]).scaled(cell_size, cell_size, Qt.KeepAspectRatio))
                    label.move(cell_size * i + ((i + 1) * 2), cell_size * j + ((j + 1) * 2))
                    label.setFixedSize(cell_size, cell_size)
                    tempList.append(label)
                    label.raise_()
                    label.show()
        
        self.repaint()
        time.sleep(1)

        for label in tempList:
            label.deleteLater()

    def update(self):
        score = read(self.game).rstrip('\n')
        self.score_lbl.setText(f'Score : {score}')
        
        board_info = read(self.game)
        cell_size = int((420 - (self.board_size + 1) * 2) / self.board_size)
        line = [board_info[i:i + self.board_size] for i in range(0, len(board_info), self.board_size)]
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j][0] != line[i][j]:
                    self.board[i][j][1].deleteLater()

                    label = QLabel(self.background)
                    label.setPixmap(QPixmap(self.img_path[line[i][j]]).scaled(cell_size, cell_size, Qt.KeepAspectRatio))
                    label.move(cell_size * i + ((i + 1) * 2), cell_size * j + ((j + 1) * 2))
                    label.setFixedSize(cell_size, cell_size)

                    self.board[i][j][0] = line[i][j]
                    self.board[i][j][1] = label
                    self.board[i][j][1].show()

        gameOver_info = read(self.game).rstrip('\n')
        if gameOver_info != 'continue':
            self.gameEnd_dialog()
        
        clear_info = read(self.game).rstrip('\n')
        if clear_info == 'clear':
            self.delete_board()
            self.create_board()

        isNew_info = read(self.game).rstrip('\n')
        if isNew_info == 'new':
            self.board_size += 1
            self.delete_board()
            self.create_board()
            self.showOnes()

    def mousePressEvent(self, event):
        if not self.isPlaying:
            return
        mousePos = self.mapFromGlobal(self.mapToGlobal(event.pos()))
        cell_size = int((420 - (self.board_size + 1) * 2) / self.board_size)
        x = mousePos.x() // (cell_size + 2)
        y = (mousePos.y() - 40) // (cell_size + 2)
        print(f'{x}, {y}')
        send(self.game, f'{x} {y}')
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

    def start(self):
        self.isPlaying = True
        self.start_btn.setEnabled(False)

        read(self.game)
        self.showOnes()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Memory_Window()
    main_window.show()
    sys.exit(app.exec_())