import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QComboBox, QGridLayout, QStackedWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from connector import *

class Minesweeper_Window(QWidget):
    CELL_SIZE = 32
    
    def load_img(self):
        src_path = os.getcwd() + '\\Mini-game-hub\\src\\minesweeper'
        self.img_path = { 'c' : src_path + '\\close.png', 'f' : src_path + '\\flag.png', }
        for i in range(0, 9):
            self.img_path[f'{i}'] = src_path + f'\\Number_{i}.png'

    def start(self, level : int):
        self.game = MINESWEEPER_EXE()
        send(self.game, f'{level}')
        if level == 0:
            self.initUI(8, 10, level)
        elif level == 1:
            self.initUI(14, 18, level)
        else:
            self.initUI(20, 24, level)
    
    def restart(self):
        self.close()
        self.__init__(self.level_select.currentIndex())
        self.show()

    def __init__(self, level : int = 0):
        super().__init__()
        self.load_img()
        self.start(level)

    def initUI(self, x : int, y : int, level : int):
        self.x = x
        self.y = y
        self.setWindowTitle("Minesweeper")
        self.setFixedSize(self.CELL_SIZE * y, self.CELL_SIZE * x + 26)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)

        hbox_info = QHBoxLayout()
        self.level_select = QComboBox(self)
        self.level_select.addItem('BEGINNER')
        self.level_select.addItem('INTERMEDIATE')
        self.level_select.addItem('ADVANCED')
        self.level_select.setCurrentIndex(level)
        self.level_select.currentIndexChanged.connect(self.level_change)
        self.level_select.setFixedWidth(130)
        hbox_info.addWidget(self.level_select, 0, Qt.AlignLeft)
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
            return
        
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
        msgBox.setWindowTitle("Game Over")
        msgBox.setText(st)
        label = msgBox.findChild(QLabel, "qt_msgbox_label")
        label.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        restartButton = QPushButton("Restart")
        msgBox.addButton(restartButton, QMessageBox.ActionRole)
        exitButton = msgBox.addButton(QMessageBox.Close)
        
        msgBox.exec_()

        if msgBox.clickedButton() == restartButton:
            self.restart()
        elif msgBox.clickedButton() == exitButton:
            self.close()

    def level_change(self):
        self.restart()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Minesweeper_Window()
    main_window.show()
    sys.exit(app.exec_())