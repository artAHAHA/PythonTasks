import re

from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QFormLayout, QPushButton, QVBoxLayout, QMessageBox


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки игры")

        self.colors_label = QLabel("Выберите цвета:")
        self.color_edits = [QLineEdit(color) for color in ['#FF0000', '#00FF00', '#0000FF', '#FFFF00']]

        # Добавим обработку события изменения текста в цветовых полях
        for edit in self.color_edits:
            edit.textChanged.connect(self.check_color_validity)

        form_layout = QFormLayout()
        form_layout.addRow(self.colors_label)
        for edit in self.color_edits:
            form_layout.addRow("Цвет:", edit)

        self.btn_ok = QPushButton("Применить")
        self.btn_ok.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.btn_ok)
        self.setLayout(layout)

    @staticmethod
    def is_valid_hex_color(color):
        """ Статический метод для проверки, является ли строка допустимым цветом в формате HEX. """
        hex_color_pattern = re.compile(r'^#[0-9A-Fa-f]{6}$')
        return bool(hex_color_pattern.match(color))

    def check_color_validity(self):
        """ Проверка каждого цвета при изменении текста в поле. """
        for edit in self.color_edits:
            color = edit.text()
            if color and not SettingsDialog.is_valid_hex_color(color):
                # Если цвет некорректен, показываем сообщение об ошибке
                edit.setStyleSheet("background-color: #FFDDDD;")  # Цвет подсветки для некорректного поля
            else:
                edit.setStyleSheet("")  # Убираем подсветку, если цвет правильный

    def get_settings(self):
        colors = [edit.text() for edit in self.color_edits]

        # Проверяем, что все введенные цвета валидны
        for color in colors:
            if not SettingsDialog.is_valid_hex_color(color):
                raise ValueError(f"Неверный цвет: {color}")

        return {
            'colors': colors
        }

    def accept(self):
        """ Переопределим accept, чтобы показывать ошибку перед применением. """
        try:
            settings = self.get_settings()
            super().accept()  # Если все в порядке, вызываем родительский accept
        except ValueError as e:
            QMessageBox.critical(self, "Ошибка", str(e))
