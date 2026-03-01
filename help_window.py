from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser

class HelpWindow(QDialog):
    def __init__(self, parent=None, lang="ru"):
        super().__init__(parent)

        titles = {
            "ru": "Справочная система",
            "en": "Help System"
        }
        self.setWindowTitle(titles.get(lang, "Справочная система"))
        self.setFixedSize(850, 800)

        layout = QVBoxLayout(self)
        self.browser = QTextBrowser()
        help_content = {
            "ru": """
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
            """,
            "en": """
            <html>
            <body style='font-family: Arial, sans-serif; font-size: 18px; line-height: 1.6; padding: 20px; color: black;'>
                <h1 style='color: black; border-bottom: 2px solid black; font-size: 24px;'>Description of implemented menu functions</h1>

                <p>Main program menu:</p>
                <p align='center'><img src='images/main_view_en.jpg' width='450'></p>

                <h2 style='color: black; font-size: 20px;'>Menu "File"</h2>
                <div style='margin-left: 20px;'>
                    <b>New</b> — creates a new document.<br>
                    <b>Open</b> — loads text from the selected file.<br>
                    <b>Save</b> — saves current changes to the open file.<br>
                    <b>Save As</b> — allows saving the document under a new name.<br>
                    <b>Exit</b> — closes the application (with a prompt to save changes).<br>
                </div>
                <p align='center'><img src='images/file_view_en.jpg' width='450'></p>

                <h2 style='color: black; font-size: 20px;'>Menu "Edit"</h2>
                <div style='margin-left: 20px;'>
                    <b>Undo</b> — reverts text to the state before the last edit.<br>
                    <b>Redo</b> — cancels the 'Undo' action.<br>
                    <b>Cut</b> — removes the selected text.<br>
                    <b>Copy</b> — copies the selected text to the clipboard.<br>
                    <b>Paste</b> — inserts text from the clipboard.<br>
                    <b>Delete</b> — clears the entire editing area.<br>
                    <b>Select All</b> — selects all text in the editing window.<br>
                </div>
                <p align='center'><img src='images/edit_view_en.jpg' width='450'></p>
            </body>
            </html>
            """
        }
        self.browser.setHtml(help_content.get(lang, help_content["ru"]))
        layout.addWidget(self.browser)