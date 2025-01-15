import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QGridLayout, QStackedWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

CELL_SIZE = 32
GROUND1 = os.getcwd() + '\\Mini-game-hub\\src\\minesweeper\\Ground1.png'
GROUND2 = os.getcwd() + '\\Mini-game-hub\\src\\minesweeper\\Ground2.png'
MASK1 = os.getcwd() + '\\Mini-game-hub\\src\\minesweeper\\Mask1.png'
MASK2 = os.getcwd() + '\\Mini-game-hub\\src\\minesweeper\\Mask2.png'

class Minesweeper_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI(8, 10, 'BEGINNER')

    def initUI(self, x, y, level):
        self.setWindowTitle("Minesweeper")
        self.setFixedSize(CELL_SIZE * y, CELL_SIZE * x + 26)

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

        self.mask_labels = []
        mask_grid = QGridLayout()
        mask_grid.setSpacing(0)
        for row in range(x):
            for col in range(y):
                label = QLabel(self)
                if (row + col) % 2 == 0:
                    label.setPixmap(QPixmap(MASK1).scaled(CELL_SIZE, CELL_SIZE, Qt.KeepAspectRatio))
                else:
                    label.setPixmap(QPixmap(MASK2).scaled(CELL_SIZE, CELL_SIZE, Qt.KeepAspectRatio))
                label.setFixedSize(CELL_SIZE, CELL_SIZE)
                mask_grid.addWidget(label, row, col)
                self.mask_labels.append(label)

        vbox.addLayout(mask_grid)

        self.setLayout(vbox)

    def mousePressEvent(self, event):
        mousePos = self.mapFromGlobal(self.mapToGlobal(event.pos()))
        y_offset = 26
        int x 
        print(f'{mousePos.x() // CELL_SIZE}, {(mousePos.y() - y_offset) // CELL_SIZE}')

        index = row * self.y + col  # 클릭된 위치의 index 계산
        if 0 <= index < len(self.mask_labels):
            mask_label = self.mask_labels[index]
            mask_label.setVisible(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Minesweeper_Window()
    main_window.show()
    sys.exit(app.exec_())