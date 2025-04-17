# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QTextBrowser, QPushButton, QVBoxLayout


class RulesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Правила игры")

        text_browser = QTextBrowser()
        text_browser.setHtml("""
            <h2>Правила игры Matching Squares</h2>
            <p>Цель игры — привести все боковые квадраты к состоянию, где все их четыре элемента одного цвета.</p>
            <ul>
                <li>Щелчок по боковому квадрату поворачивает его цвета по часовой стрелке.</li>
                <li>Щелчок по центральному квадрату инициирует передачу угловых цветов между квадратами по кругу.</li>
                <li>Вы побеждаете, когда все 4 квадрата имеют однородные цвета.</li>
            </ul>
        """)

        btn_close = QPushButton("Закрыть")
        btn_close.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(text_browser)
        layout.addWidget(btn_close)
        self.setLayout(layout)
