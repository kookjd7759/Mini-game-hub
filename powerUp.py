import sys
import time
import os

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QThread, QTimer, QPoint, QPropertyAnimation, QEventLoop, QRect
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QFont

from PIL import Image



def image_to_pixmap(image, reverse, cut48to32):
    if reverse:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    if cut48to32:
        width, height = image.size
        left = 8
        top = 0
        right = width - 8
        bottom = height - 16
        image = image.crop((left, top, right, bottom))
    image = image.convert("RGBA")
    data = image.tobytes("raw", "RGBA")
    qimage = QImage(data, image.width, image.height, QImage.Format_RGBA8888)
    pixmap = QPixmap.fromImage(qimage)
    return pixmap

def path_to_pixmap(path):
    image = Image.open(path)
    return image_to_pixmap(image, False, False)

def split_image(image_path, num_splits, reverse = False, cut48to32 = False):
    image = Image.open(image_path)
    w, h = image.size

    slice_w = w // num_splits
    images = []
    for i in range(num_splits):
        left = i * slice_w
        right = (i + 1) * slice_w if i < num_splits - 1 else w
        box = (left, 0, right, h)
        sliced = image.crop(box)
        images.append(image_to_pixmap(sliced, reverse, cut48to32))

    return images



class Object_Thread(QThread):
    def __init__(self, images : list, label, interval=100):
        super().__init__()
        self.images = images
        self.label = label
        self.interval = interval

        self.cur_idx = 0
        pixmap = self.images[0]
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.width(), pixmap.height())

    def run(self):
        while True:
            self.label.setPixmap(self.images[self.cur_idx])
            self.cur_idx = (self.cur_idx + 1) % len(self.images)
            time.sleep(self.interval / 1000)



class GaugeBar(QWidget):
    def __init__(self, max, cur, parent=None):
        super().__init__(parent)
        self.max = max
        self.cur = cur

    def set(self, data):
        self.cur = max(0, min(data, self.max))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setPen(QColor(0, 0, 0))
        font = QFont()
        font.setPointSize(6)
        font.setBold(True)
        painter.setFont(font)

        text_rect = QRect(0, 0, 32, 6)
        painter.drawText(text_rect, Qt.AlignCenter, 'Player')

        background = QRect(0, 10, 32, 4)
        painter.setBrush(QColor(240, 240, 240))
        painter.setPen(QColor(0, 0, 0))
        painter.drawRoundedRect(background, 2, 2)

        bar_rect = QRect(0, 11, int(self.cur / self.max * 32), 4)
        painter.setBrush(QColor(255, 0, 0))
        painter.drawRoundedRect(bar_rect, 2, 2)



class Player_Thread(QThread):
    HP = 100
    ATK = 10
    def __init__(self, images : dict, label, interval=100):
        super().__init__()
        self.images = images
        self.label = label
        self.interval = interval
        
        self.cur_idx = 0
        self.cur_state = 'D_Idle'
        pixmap = self.images[self.cur_state][0]
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.width(), pixmap.height())

    def run(self):
        while True:
            self.label.setPixmap(self.images[self.cur_state][self.cur_idx])
            self.label.raise_()
            self.cur_idx = (self.cur_idx + 1) % len(self.images[self.cur_state])
            time.sleep(self.interval / 1000)

    def change_state(self, state):
        if state != self.cur_state:
            self.cur_state = state
            self.cur_idx = 0


class Unit(QWidget):
    def __init__(self, images, name, level, HP, ATK, parent=None):
        super().__init__(parent)
        self.images = images
        self.name = name
        self.level = level
        self.HP = HP
        self.ATK = ATK
    
    def initUI(self):
        print('TODO')




class PowerUpWindow(QWidget):
    CELL_SIZE = 32
    move_speed = 600
    isMoving = False

    def load_img(self):
        src_path = os.getcwd() + '\\Mini-game-hub\\image\\power up'
        self.player_images = {
            'D_Idle': split_image(f'{src_path}\\player\\D_Idle.png', 4, cut48to32=True),
            'D_Walk': split_image(f'{src_path}\\player\\D_Walk.png', 6, cut48to32=True),
            'U_Idle': split_image(f'{src_path}\\player\\U_Idle.png', 4, cut48to32=True),
            'U_Walk': split_image(f'{src_path}\\player\\U_Walk.png', 6, cut48to32=True),
            'L_Idle': split_image(f'{src_path}\\player\\S_Idle.png', 4, cut48to32=True),
            'L_Walk': split_image(f'{src_path}\\player\\S_Walk.png', 6, cut48to32=True),
            'R_Idle': split_image(f'{src_path}\\player\\S_Idle.png', 4, reverse=True, cut48to32=True),
            'R_Walk': split_image(f'{src_path}\\player\\S_Walk.png', 6, reverse=True, cut48to32=True)
        }
        self.slime_images = {
            'D_Idle': split_image(f'{src_path}\\player\\D_Idle.png', 4, cut48to32=True),
        }
        self.tile_images = {
            'gress' : path_to_pixmap(f'{src_path}\\tile\\ground_gress.png')
        }

    def __init__(self):
        super().__init__()
        self.load_img()
        self.initUI()

        self.one_move_timer = QTimer(self)
        self.one_move_timer.setSingleShot(True)
        self.one_move_timer.timeout.connect(self.one_move_timeout)

        self.player_lbl = QLabel(self)
        self.player_lbl.move(self.CELL_SIZE * 1, self.CELL_SIZE * 1)
        self.state = 'D_Idle'
        self.player = Player_Thread(self.player_images, self.player_lbl)
        self.player.start()
        
        self.player_bar = GaugeBar(100, 100, self)
        self.player_bar.move(self.CELL_SIZE * 1, self.CELL_SIZE * 1 - 16)
        

    def initUI(self):
        self.setWindowTitle("Power up !")
        self.setFixedSize(320, 320)

        layout = QVBoxLayout()
        self.background = []
        self.create_background()

        self.setLayout(layout)

    def one_move_timeout(self):
        self.isMoving = False
        self.change_state(f'{self.state[0]}_Idle')

    def create_background(self):
        for img in self.background:
            img.deleteLater()
        self.background = []

        for i in range(10):
            for j in range(10):
                ground = QLabel(self)
                pixmap = self.tile_images['gress']
                ground.setPixmap(pixmap)
                ground.resize(pixmap.width(), pixmap.height())
                ground.move(self.CELL_SIZE * i, self.CELL_SIZE * j)
                self.background.append(ground)

    def change_state(self, state):
        if self.state != state:
            self.state = state
            self.player.change_state(self.state)
    
    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_S, Qt.Key_W, Qt.Key_D, Qt.Key_A]:
            if self.isMoving:
                return
            self.isMoving = True

            dir = 'D' if event.key() == Qt.Key_S else 'U' if event.key() == Qt.Key_W else \
                'R' if event.key() == Qt.Key_D else 'L'
            self.change_state(f'{dir}_Walk')
            self.one_move_timer.start(self.move_speed)
            self.move_player(self.move_speed, dir)

        if event.key() == Qt.Key_Space:
            print(f'HP  : {self.player.HP}')
            print(f'ATK : {self.player.ATK}')
    
    def move_player(self, duration, dir):
        player_start = self.player_lbl.pos()
        player_dest = None
        if dir == 'U':
            player_dest = QPoint(player_start.x(), player_start.y() - self.CELL_SIZE)
        elif dir == 'D':
            player_dest = QPoint(player_start.x(), player_start.y() + self.CELL_SIZE)
        elif dir == 'L':
            player_dest = QPoint(player_start.x() - self.CELL_SIZE, player_start.y())
        elif dir == 'R':
            player_dest = QPoint(player_start.x() + self.CELL_SIZE, player_start.y())
        player_animation = QPropertyAnimation(self.player_lbl, b"pos")
        player_animation.setDuration(duration)
        player_animation.setStartValue(player_start)
        player_animation.setEndValue(player_dest)

        bar_start = self.player_bar.pos()
        bar_dest = QPoint(player_dest.x(), player_dest.y() - 16)
        bar_animation = QPropertyAnimation(self.player_bar, b"pos")
        bar_animation.setDuration(duration)
        bar_animation.setStartValue(bar_start)
        bar_animation.setEndValue(bar_dest)

        loop = QEventLoop()
        player_animation.finished.connect(loop.quit)
        player_animation.start()
        bar_animation.finished.connect(loop.quit)
        bar_animation.start()
        loop.exec_()
        self.player_lbl.move(player_dest.x(), player_dest.y())
        self.player_bar.move(bar_dest.x(), bar_dest.y())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = PowerUpWindow()
    main_window.show()
    sys.exit(app.exec_())
