# from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QHBoxLayout, QWidget, QVBoxLayout
from PyQt6 import QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import *
import PyQt6.QtGui
import sys
import os.path
from time import sleep

heroes_ability = {
    'ABADDON': ['time', 60, 50, 40]
}
for i in heroes_ability:
    print(i)
class Hero(QThread):
    def __init__(self, hero, skill_lvl):
        super(QThread, self).__init__(None)

        self.hero = hero
        self.skill_lvl = skill_lvl
        self.ico = QLabel()
        self.widg = QWidget()
        self.layout = QVBoxLayout()
        self.widg.setLayout(self.layout)
        self.path = 'icons/' + self.hero + '.png'
        self.ico.setPixmap(PyQt6.QtGui.QPixmap(self.path))
        # ability
        self.ability_timer = QLabel()

        self.test_label = QLabel()
        self.test_label.setPixmap(PyQt6.QtGui.QPixmap('icons/' + 'rosh' + '.png'))
        # buttons and etc.
        self.submit_button = QPushButton('submit\nhero')
        self.submit_button.setStyleSheet("background-color: #e0a96d")
        self.start_ability_button = QPushButton('V')
        self.start_ability_button.setStyleSheet("background-color: #e0a96d")
        self.choose_box = QComboBox()
        self.choose_box.addItems(['rosh', 'enigma'])
        for hero in heroes_ability:
            self.choose_box.addItem(hero)
        self.choose_box.setStyleSheet("background-color: #e0a96d")

        self.stop_ability_button = QPushButton('X')
        self.stop_ability_button.setStyleSheet("background-color: #e0a96d")
        # layout adds
        self.layout.addWidget(self.ico)
        # self.layout.addWidget(self.test_label)
        self.layout.addWidget(self.start_ability_button)
        self.layout.addWidget(self.stop_ability_button)
        self.layout.addWidget(self.choose_box)
        self.layout.addWidget(self.submit_button)

        self.is_running = False
        self.can_start = True

    def run(self):
        self.hero = self.choose_box.currentText()
        self.path = 'icons/' + self.hero + '.png'
        print(os.path.exists(self.path))
        if os.path.exists(self.path):
            self.ico.setPixmap(PyQt6.QtGui.QPixmap(self.path))
        else:
            self.ico.setPixmap(PyQt6.QtGui.QPixmap('icons/no_ico.png'))


    def rosh_start(self):
        self.time_left_int = 60 * 11
        if self.can_start:
            self.can_start = False
            self.rosh_timer = QtCore.QTimer(self)
            self.rosh_timer.timeout.connect(self.rosh_timeout)
            self.rosh_timer.start(1000)
            self.rosh_timer_text.setText(f'Rosh time: {self.time_left_int // 60}:{self.time_left_int % 60}')

    def rosh_timeout(self):
        self.time_left_int -= 1
        self.rosh_timer_text.setText(f'Rosh time: {self.time_left_int // 60}:{self.time_left_int % 60}')
        if self.time_left_int <= 0:
            self.rosh_stop()
        print(self.time_left_int)

    def rosh_stop(self):
        if self.can_start == False:
            self.rosh_timer.stop()
            self.can_start = True
            self.rosh_timer_text.setText('Rosh is alive')
            print('stopped')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dota2timer')
        # self.setFixedSize(800, 700)
        self.setMaximumSize(500, 10000)
        self.setMinimumSize(0, 550)

        self.rosh_ico = QLabel()
        # Layouts
        self.layout_rosh = QHBoxLayout()
        self.layout_heroes = QHBoxLayout()

        self.rosh_timer_text = QLabel('qewwe')
        self.rosh_button_start = QPushButton('Rosh killed')
        self.rosh_button_cans = QPushButton('X')
        self.timer = QTimer()
        self.pixmap = PyQt6.QtGui.QPixmap('icons/rosh.png')
        self.smaller_pixmap = self.pixmap.scaled(85, 85)

        # heroes
        self.hero_1 = Hero('rosh', 1)
        self.hero_2 = Hero('rosh', 1)
        self.hero_3 = Hero('enigma', 1)
        self.hero_4 = Hero('rosh', 1)

        # heroes layout
        self.layout_heroes.addWidget(self.hero_1.widg)
        self.layout_heroes.addWidget(self.hero_2.widg)
        self.layout_heroes.addWidget(self.hero_3.widg)
        self.layout_heroes.addWidget(self.hero_4.widg)
        # heroes buttons
        self.hero_1.submit_button.clicked.connect(self.hero_1.start)
        self.hero_2.submit_button.clicked.connect(self.hero_2.start)
        self.hero_3.submit_button.clicked.connect(self.hero_3.start)
        self.hero_4.submit_button.clicked.connect(self.hero_4.start)

        # roshan
        self.rosh_button_start.setStyleSheet("background-color: #e0a96d")
        self.rosh_button_cans.setStyleSheet("background-color: #e0a96d")
        self.rosh_timer_text.setStyleSheet("color: #e0a96d")
        self.rosh_ico.setPixmap(self.smaller_pixmap)

        self.layout_rosh.addWidget(self.rosh_ico)
        self.layout_rosh.addWidget(self.rosh_timer_text)
        self.layout_rosh.addWidget(self.rosh_button_start)
        self.layout_rosh.addWidget(self.rosh_button_cans)

        self.rosh_button_start.clicked.connect(self.rosh_start)
        self.rosh_button_cans.clicked.connect(self.rosh_stop)
        self.rosh_timer_text.setText('Rosh is alive')

        # containers
        container_main = QWidget()
        container_main.setLayout(self.layout_heroes)
        # container_main.setStyleSheet("background-color: wheat")

        container_rosh = QWidget()
        container_rosh.setLayout(self.layout_rosh)
        container_rosh.setStyleSheet("background-color: #292629")

        self.setMenuWidget(container_rosh)
        self.setCentralWidget(container_main)

        self.can_start = True

    def rosh_start(self):
        self.time_left_int = 60 * 11
        if self.can_start:
            self.can_start = False
            self.rosh_timer = QtCore.QTimer(self)
            self.rosh_timer.timeout.connect(self.rosh_timeout)
            self.rosh_timer.start(1000)
            self.rosh_timer_text.setText(f'Rosh time: {self.time_left_int // 60}:{self.time_left_int % 60}')

    def rosh_timeout(self):
        self.time_left_int -= 1
        self.rosh_timer_text.setText(f'Rosh time: {self.time_left_int // 60}:{self.time_left_int % 60}')
        if self.time_left_int <= 0:
            self.rosh_stop()
        print(self.time_left_int)

    def rosh_stop(self):
        if self.can_start == False:
            self.rosh_timer.stop()
            self.can_start = True
            self.rosh_timer_text.setText('Rosh is alive')
            print('stopped')


app = QApplication(sys.argv)  # Передаём sys.argv, чтобы разрешить аргументы командной строки для приложения.

window = MainWindow()
window.setStyleSheet("background-color: #201e20")
window.show()

# Hex code: #ddc3a5, #201e20, #e0a96d

app.exec()  # Запускаем цикл событий.
print('end')
# Приложение не доберётся сюда, пока вы не выйдете и цикл
# событий не остановится.
