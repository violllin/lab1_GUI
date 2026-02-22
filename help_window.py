from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser


class HelpWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Справочная система")
        self.setFixedSize(850, 800)

        layout = QVBoxLayout(self)
        self.browser = QTextBrowser()

        help_html = """
        <html>
        <body style='font-family: Arial, sans-serif; font-size: 18px; line-height: 1.6; padding: 20px; color: black;'>
            <h1 style='color: black; border-bottom: 2px solid black; font-size: 24px;'>Описание реализованных функций меню</h1>

            <p>Главное меню программы:</p>
            <p align='center'><img src='images/main_view.jpg' width='450'></p>

            <h2 style='color: black; font-size: 20px;'>Меню "Файл"</h2>
            <div style='margin-left: 20px;'>
                <b>Создать</b> — создает новый документ.<br>
                <b>Открыть</b> — загружает текст из выбранного файла.<br>
                <b>Сохранить</b> — сохраняет текущие изменения в открытый файл.<br>
                <b>Сохранить как</b> — позволяет сохранить документ под новым именем.<br>
                <b>Выход</b> — закрывает приложение (с предложением сохранить изменения).<br>
            </div>
            <p align='center'><img src='images/file_view.jpg' width='450'></p>

            <h2 style='color: black; font-size: 20px;'>Меню "Правка"</h2>
            <div style='margin-left: 20px;'>
                <b>Отменить</b> — возвращает текст к состоянию до последней правки.<br>
                <b>Повторить</b> — отменяет действие кнопки 'Отменить'.<br>
                <b>Вырезать</b> — удаляет выделенный текст.<br>
                <b>Копировать</b> — копирует выделенный текст в буфер обмена.<br>
                <b>Вставить</b> — вставляет текст из буфера обмена.<br>
                <b>Удалить</b> — очищает всю область редактирования.<br>
                <b>Выделить все</b> — выделяет весь текст в окне редактирования.<br>
            </div>
            <p align='center'><img src='images/edit_view.jpg' width='450'></p>
        </body>
        </html>
        """

        self.browser.setHtml(help_html)
        layout.addWidget(self.browser)