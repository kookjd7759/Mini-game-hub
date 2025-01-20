import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap

from connector import *

class Thread(QThread):
    output_signal = pyqtSignal(str)

    def __init__(self, parent, game):
        super().__init__(parent)
        self.game = game

    def run(self):
        signal = read(self.game).rstrip('\n')
        self.output_signal.emit(signal)
                

class Click_Window(QWidget):
    isclickable = False
    isStartClick = True
    isMeasureClick = False
    isWating = False
    count = 0
    
    def closeEvent(self, event):
        if self.game:
            self.game.terminate()
            self.game.wait()
        event.accept()
        
    def restart(self):
        self.close()
        if self.waiting_thread.isRunning():
            print('!!!')
            self.waiting_thread.terminate()
            self.waiting_thread.wait()
        self.isclickable = False
        self.isStartClick = True
        self.isMeasureClick = False
        self.isWating = False
        self.count = 0
        self.__init__()
        self.show()

    def load_img(self):
        src_path = os.getcwd() + '\\Mini-game-hub\\image\\click'
        self.icon_path  = src_path + '\\icon.png'
        self.img_path = { 
            'on' : src_path + '\\on.png',
            'off' : src_path + '\\off.png'
            }

    def switch_bg(self):
        if self.background_state == 'on':
            self.background_state = 'off'
            self.background.setPixmap(QPixmap(self.img_path['off']).scaled(480, 270))
        else:
            self.background_state = 'on'
            self.background.setPixmap(QPixmap(self.img_path['on']).scaled(480, 270))
    
    def update(self):
        if not self.isWating: 
            return
        self.switch_bg()
        self.isWating = False

    def __init__(self):
        super().__init__()
        self.load_img()
        self.game = CLICK_EXE()
        self.initUI()
        self.waiting_thread = Thread(self, self.game)
        self.waiting_thread.output_signal.connect(self.update)

    def initUI(self):
        self.setWindowTitle("Click !")
        self.setWindowIcon(QIcon(self.icon_path))
        self.setFixedSize(480, 270 + 29)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)

        hbox = QHBoxLayout()
        self.size_select = QComboBox(self)
        self.size_select.addItem('3')
        self.size_select.addItem('5')
        self.size_select.addItem('10')
        self.size_select.setCurrentIndex(0)
        self.size_select.setFixedWidth(100)
        hbox.addWidget(self.size_select, 0, Qt.AlignRight)

        self.start_btn = QPushButton('Start')
        self.start_btn.setFixedWidth(200)
        self.start_btn.clicked.connect(self.start)
        hbox.addWidget(self.start_btn)
        vbox.addLayout(hbox)

        self.background_state = 'on'
        self.background = QLabel(self)
        self.background.setAttribute(Qt.WA_OpaquePaintEvent)
        self.background.setPixmap(QPixmap(self.img_path['on']).scaled(480, 270))
        self.background.setEnabled(False)
        vbox.addWidget(self.background)
        
        self.setLayout(vbox)

    def mousePressEvent(self, event):
        if not self.isclickable:
            return 
        
        if self.isStartClick:
            self.switch_bg()
            send(self.game, '0')
            self.isStartClick = False
            self.isMeasureClick = True
            self.isWating = True
            self.waiting_thread.start()
        elif self.isMeasureClick:
            if self.isWating:
                self.isWating = False
                self.gameEnd_dialog('Failed', 'Don\'t click on the prediction ...')
                return
            self.switch_bg()
            self.count += 1
            send(self.game, '0')
            self.isStartClick = True
            self.isMeasureClick = False
            score = read(self.game).rstrip('\n')
            msgBox = QMessageBox(self)
            msgBox.setWindowTitle("Score")
            msgBox.setText(score)
            msgBox.exec_()
            self.switch_bg()
        
        if self.count == int(self.size_select.currentText()):
            average_score = read(self.game).rstrip('\n')
            self.gameEnd_dialog('Complete', average_score)


    def gameEnd_dialog(self, title, st):
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle(title)
        msgBox.setText(st)
        
        restartButton = QPushButton("Restart")
        msgBox.addButton(restartButton, QMessageBox.ActionRole)
        exitButton = msgBox.addButton(QMessageBox.Close)
        
        msgBox.exec_()

        if msgBox.clickedButton() == restartButton:
            self.restart()
        elif msgBox.clickedButton() == exitButton:
            self.close()

    def start(self):
        self.background.setEnabled(True)
        self.size_select.setEnabled(False)
        self.start_btn.setEnabled(False)
        size = int(self.size_select.currentText())
        send(self.game, f'{size}')
        self.isclickable = True



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Click_Window()
    main_window.show()
    sys.exit(app.exec_())