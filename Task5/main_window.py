# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Task5.game import Game
from Task5.rules import RulesDialog
from Task5.settings import SettingsDialog
from Task5.square_widget import SquareWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game = Game()
        self.square_widgets = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Matching Squares")
        self.setGeometry(200, 200, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        game_area = QWidget()
        game_area.setFixedSize(600, 600)
        layout.addWidget(game_area, alignment=Qt.AlignCenter)

        menu = self.menuBar()
        game_menu = menu.addMenu("Меню")

        rules_action = QAction("Правила", self)
        rules_action.triggered.connect(self.show_rules)
        game_menu.addAction(rules_action)

        settings_action = QAction("Настройки", self)
        settings_action.triggered.connect(self.show_settings)
        game_menu.addAction(settings_action)

        # Позиции для 4 квадратов в 2 ряда
        positions = [
            (100, 100),  # Верхний левый (1)
            (300, 100),  # Верхний правый (2)
            (300, 300),  # Нижний правый (3)
            (100, 300)   # Нижний левый (4)
        ]

        # Сначала создаем 4 виджета с маленькими квадратами
        for i in range(4):
            widget = SquareWidget(self.game.circles[i], i + 1)
            widget.setParent(game_area)
            widget.move(positions[i][0], positions[i][1])
            widget.clicked.connect(self.rotate_square)
            self.square_widgets.append(widget)

        # Затем центральный квадрат (он должен быть сверху)
        central = SquareWidget(self.game.circles[0], 0, is_central=True)
        central.setParent(game_area)
        central.move(200, 200)
        central.clicked.connect(self.rotate_square)
        self.square_widgets.insert(0, central)

        # Кнопка новой игры
        self.btn_reset = QPushButton("Новая игра")
        layout.addWidget(self.btn_reset, alignment=Qt.AlignCenter)
        self.btn_reset.clicked.connect(self.new_game)

    def rotate_square(self, index):
        if index == 0:
            # Последовательность передвижения:
            chain = [
                (0, 1),  # правый нижний угол верхнего левого
                (1, 2),  # левый нижний угол верхнего правого
                (2, 3),  # левый верхний угол нижнего правого
                (3, 0)  # правый верхний угол нижнего левого
            ]

            # Сохраняем значение последнего
            temp = self.game.circles[chain[-1][0]][chain[-1][1]]

            # Передвигаем значения по кругу в обратном порядке
            for i in reversed(range(1, len(chain))):
                from_idx = chain[i - 1]
                to_idx = chain[i]
                self.game.circles[to_idx[0]][to_idx[1]] = self.game.circles[from_idx[0]][from_idx[1]]

            # Возвращаем temp в первую позицию
            self.game.circles[chain[0][0]][chain[0][1]] = temp

            # Обновляем виджеты
            for i in range(1, 5):
                self.square_widgets[i].colors = self.game.circles[i - 1]
                self.square_widgets[i].update()

            self.game.check_win()
            if self.game.is_win:
                QMessageBox.information(self, "Победа!", "Все цвета совпадают с центральным квадратом!")

        elif index > 0:
            self.game.rotate(index - 1)
            self.square_widgets[index].colors = self.game.circles[index - 1]
            self.square_widgets[index].update()
            if self.game.is_win:
                QMessageBox.information(self, "Победа!", "Все цвета совпадают с центральным квадратом!")

    def new_game(self):
        self.game.reset()
        for i in range(5):
            self.square_widgets[i].colors = self.game.circles[i - 1 if i > 0 else 0]
            self.square_widgets[i].update()

    def show_rules(self):
        dlg = RulesDialog(self)
        dlg.exec_()

    def show_settings(self):
        dlg = SettingsDialog(self)
        if dlg.exec_():
            settings = dlg.get_settings()
            self.game.colors = settings['colors']
            self.new_game()

