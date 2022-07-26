# from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QHBoxLayout, QWidget, QVBoxLayout
from PyQt6 import QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import *
import PyQt6.QtGui
import sys
import os.path
from win10toast import ToastNotifier
from time import sleep

items_dict = {
    'SPELL_PRISM': 13,
    'WTF_ASPECT1': 11,
    'WTF_ASPECT2': 10
}

heroes_ability = {
    'ABADDON': ['time', 60, 50, 40],
    'ROSH': ['time', 5, 29, 28],
    'ENIGMA': ['time', 20, 19, 18]
}


class Choose_Item_Window(QMainWindow):
    def __init__(self):
        super(Choose_Item_Window, self).__init__()
        # windows settings
        self.setFixedSize(320, 160)
        self.layout = QVBoxLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        # widgets
        self.text_info = QLabel()
        self.text_info.setText('Choose item')
        self.text_info.setStyleSheet('color: #e0a96d')
        self.all_items_box = QComboBox()
        self.all_items_box.setStyleSheet('background-color: #e0a96d')
        self.submit_button = QPushButton('Submit')
        self.submit_button.setStyleSheet('background-color: #e0a96d')
        self.close_button = QPushButton('Close')
        self.close_button.setStyleSheet('background-color: #e0a96d')
        # create items box
        for itm in items_dict:
            self.all_items_box.addItem(itm)
        # adds
        self.layout.addWidget(self.text_info)
        self.layout.addWidget(self.all_items_box)
        self.layout.addWidget(self.submit_button)
        self.layout.addWidget(self.close_button)


class Hero(QThread):
    def __init__(self, hero, ability_lvl):
        super(QThread, self).__init__(None)

        self.hero = hero
        self.ability_lvl = ability_lvl
        self.ico = QLabel()
        self.widg = QWidget()
        self.layout = QVBoxLayout()
        self.widg.setLayout(self.layout)
        self.path = 'icons/' + self.hero + '.png'
        self.ico.setPixmap(PyQt6.QtGui.QPixmap(self.path))
        # items
        self.items_title = QLabel()
        self.items_title.setText('Items')
        self.items_title.setStyleSheet('color: #e0a96d')
        self.choose_item_window = Choose_Item_Window()
        self.choose_item_window.setStyleSheet('background-color: #201e20')
        self.items_added_list = []
        # buttons 4 items and etc
        self.add_item_button = QPushButton('Add item')
        self.add_item_button.setStyleSheet('background-color: #e0a96d')
        self.add_item_button.clicked.connect(self.choose_item_window.show)
        self.delete_item_button = QPushButton('Delete this\nitem')
        self.delete_item_button.setStyleSheet('background-color: #e0a96d')
        self.delete_item_button.clicked.connect(self.del_item)
        self.item_box = QComboBox()
        self.item_box.setStyleSheet('background-color: #e0a96d')
        self.submit_item_button = self.choose_item_window.submit_button
        self.submit_item_button.clicked.connect(self.add_item)
        self.close_item_window_button = self.choose_item_window.close_button
        self.close_item_window_button.clicked.connect(self.choose_item_window.close)
        # ability
        self.ability_timer_text = QLabel()
        self.ability_timer_text.setStyleSheet('color: #e0a96d')
        self.ability_timer_text.setText('Ability can be used')
        # buttons 4 abilities and etc.
        self.submit_button = QPushButton('submit\nhero')
        self.submit_button.setStyleSheet('background-color: #e0a96d')
        self.submit_button.clicked.connect(self.change_hero)
        self.start_ability_button = QPushButton('V ability')
        self.start_ability_button.setStyleSheet('background-color: #e0a96d')
        self.stop_ability_button = QPushButton('X ability')
        self.stop_ability_button.setStyleSheet('background-color: #e0a96d')
        self.stop_ability_button.clicked.connect(self.stop_ability)
        self.choose_box = QComboBox()
        self.choose_box.setStyleSheet('background-color: #e0a96d')
        for hero in heroes_ability:  # add all heroes to choose_box from heroes_ability dictionary
            self.choose_box.addItem(hero)
        # layout adds
        self.layout.addWidget(self.ico)
        self.layout.addWidget(self.ability_timer_text)
        self.layout.addWidget(self.start_ability_button)
        self.layout.addWidget(self.stop_ability_button)
        self.layout.addWidget(self.choose_box)
        self.layout.addWidget(self.submit_button)
        self.layout.addWidget(self.items_title)
        self.layout.addWidget(self.item_box)
        self.layout.addWidget(self.delete_item_button)
        self.layout.addWidget(self.add_item_button)

        self.notif = ToastNotifier()
        self.ability_cooldown = 0
        self.is_running = False

    def add_item(self):
        self.stop_ability()
        item = self.choose_item_window.all_items_box.currentText()
        if not (item in self.items_added_list):
            self.items_added_list.append(item)
            self.item_box.addItem(item)
            print(self.items_added_list)
        else:
            self.choose_item_window.text_info.setText('This item is already taken')
        self.update_ability_cooldown()

    def del_item(self):
        self.stop_ability()
        item = self.item_box.currentText()
        self.item_box.removeItem(self.item_box.currentIndex())
        self.items_added_list.pop(self.items_added_list.index(item))
        self.update_ability_cooldown()

    def update_ability_cooldown(self):
        all_items = 1
        for el in self.items_added_list:
            all_items *= 1 - items_dict[el] * 0.01
        print(all_items)
        self.ability_cooldown = heroes_ability[self.hero][self.ability_lvl] * all_items
        self.ability_timer_text.setText(f'Ability can be used\n{self.ability_cooldown} sec.')

    def stop_ability(self):
        self.is_running = False
        self.terminate()
        self.update_ability_cooldown()

    def run(self):
        self.is_running = True
        self.update_ability_cooldown()
        sleep(1)
        while self.ability_cooldown > 0:
            self.ability_timer_text.setText(f'Ability cooldown:\n' + str(self.ability_cooldown) + ' sec.')
            self.ability_cooldown -= 1
            sleep(1)
        self.update_ability_cooldown()
        self.is_running = False
        try:
            self.notif.show_toast('Dota timer', f'{self.hero} ability is available')
        except Exception:
            pass

    def change_hero(self):
        self.stop_ability()
        self.hero = self.choose_box.currentText()
        print(f'hero changed:{self.hero}')
        self.path = 'icons/' + self.hero.lower() + '.png'
        print(f'new path: {self.path}')
        self.update_ability_cooldown()
        print('cooldown updated')
        print(os.path.exists(self.path))
        if os.path.exists(self.path):
            self.ico.setPixmap(PyQt6.QtGui.QPixmap(self.path))
        else:
            self.ico.setPixmap(PyQt6.QtGui.QPixmap('icons/no_ico.png'))

    # # через QTimer. как появится интернет, надо погуглить, как его починить с потоками
    # def run(self):  # was rosh_start
    #     print('должно начаться')
    #     self.time_left_int = heroes_ability[self.hero][self.ability_lvl]
    #     if self.can_start:
    #         self.can_start = False
    #         self.ability_timer = QtCore.QTimer(self) # was rosh_timer
    #         self.ability_timer.timeout.connect(self.ability_timeout)
    #         self.ability_timer.start(1000)
    #         self.ability_timer_text.setText(f'Time remaining: {self.time_left_int // 60}:{self.time_left_int % 60}')
    #
    # def ability_timeout(self):
    #     self.time_left_int -= 1
    #     self.ability_timer_text.setText(f'Time remaining: {self.time_left_int // 60}:{self.time_left_int % 60}')
    #     if self.time_left_int <= 0:
    #         self.ability_stop()
    #     print(self.time_left_int)
    #
    # def ability_stop(self):
    #     if self.can_start == False:
    #         self.ability_timer.stop()
    #         self.can_start = True
    #         self.ability_timer_text.setText('Rosh is alive')
    #         print('stopped')


class Main_Window(QMainWindow):
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
        self.hero_1 = Hero('ROSH'.upper(), 1)
        self.hero_2 = Hero('ROSH'.upper(), 1)
        self.hero_3 = Hero('ROSH'.upper(), 1)
        self.hero_4 = Hero('ROSH'.upper(), 1)
        self.hero_5 = Hero('ROSH'.upper(), 1)
        # heroes layout
        self.layout_heroes.addWidget(self.hero_1.widg)
        self.layout_heroes.addWidget(self.hero_2.widg)
        self.layout_heroes.addWidget(self.hero_3.widg)
        self.layout_heroes.addWidget(self.hero_4.widg)
        self.layout_heroes.addWidget(self.hero_5.widg)
        # heroes buttons
        self.hero_1.start_ability_button.clicked.connect(self.hero_1.start)
        self.hero_2.start_ability_button.clicked.connect(self.hero_2.start)
        self.hero_3.start_ability_button.clicked.connect(self.hero_3.start)
        self.hero_4.start_ability_button.clicked.connect(self.hero_4.start)
        self.hero_5.start_ability_button.clicked.connect(self.hero_5.start)
        # roshan
        self.rosh_button_start.setStyleSheet('background-color: #e0a96d')
        self.rosh_button_cans.setStyleSheet('background-color: #e0a96d')
        self.rosh_timer_text.setStyleSheet('color: #e0a96d')
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

        container_rosh = QWidget()
        container_rosh.setLayout(self.layout_rosh)
        container_rosh.setStyleSheet('background-color: #292629')

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

    def rosh_stop(self):
        if self.can_start == False:
            self.rosh_timer.stop()
            self.can_start = True
            self.rosh_timer_text.setText('Rosh is alive')
            print('stopped')


app = QApplication(sys.argv)  # Передаём sys.argv, чтобы разрешить аргументы командной строки для приложения.

window = Main_Window()
window.setStyleSheet('background-color: #201e20')
window.show()
# Hex code: #ddc3a5, #201e20, #e0a96d

app.exec()  # Запускаем цикл событий.
print('end')
# Приложение не доберётся сюда, пока вы не выйдете и цикл
# событий не остановится.
