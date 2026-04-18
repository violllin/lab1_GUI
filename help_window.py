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
                <h1 style='color: black; border-bottom: 2px solid black; font-size: 24px;'>Описание реализованных функций программы</h1>

                <p>Главное окно программы с рабочей областью и таблицей результатов:</p>
                <p align='center'><img src='images/help/main_window.jpg' width='450'></p>

                <h2 style='color: black; font-size: 20px;'>Меню "Файл"</h2>
                <div style='margin-left: 20px;'>
                    <b>Создать</b> — создает новый документ и открывает его в новой вкладке.<br>
                    <b>Открыть</b> — загружает текст из выбранного файла.<br>
                    <b>Сохранить</b> — сохраняет текущие изменения в открытом файле.<br>
                    <b>Сохранить как</b> — позволяет сохранить документ под новым именем.<br>
                    <b>Выход</b> — закрывает приложение (с предложением сохранить изменения).<br>
                </div>
                <p align='center'><img src='images/help/menu_file.jpg' width='450'></p>

                <h2 style='color: black; font-size: 20px;'>Меню "Правка"</h2>
                <div style='margin-left: 20px;'>
                    <b>Отменить</b> — возвращает текст к состоянию до последнего изменения.<br>
                    <b>Повторить</b> — отменяет действие 'Отменить'.<br>
                    <b>Вырезать</b> — удаляет выделенный текст и помещает его в буфер обмена.<br>
                    <b>Копировать</b> — копирует выделенный текст в буфер обмена.<br>
                    <b>Вставить</b> — вставляет текст из буфера обмена.<br>
                    <b>Удалить</b> — очищает выделенный фрагмент текста.<br>
                    <b>Выделить все</b> — выделяет весь текст в текущем окне редактирования.<br>
                </div>
                <p align='center'><img src='images/help/menu_edit.jpg' width='450'></p>

                <h2 style='color: black; font-size: 20px;'>Меню "Текст"</h2>
                <div style='margin-left: 20px;'>
                    <b>Постановка задачи</b> — открывает окно с описанием задания к курсовой работе.<br>
                    <b>Грамматика</b> — отображает правила грамматики для лямбда-выражений языка Swift.<br>
                    <b>Классификация грамматики</b> — выводит информацию о типе используемой грамматики.<br>
                    <b>Метод анализа</b> — описание алгоритма работы синтаксического анализатора.<br>
                    <b>Диагностика и нейтрализация ошибок</b> — справка по механизму отлова ошибок.<br>
                    <b>Тестовый пример</b> — загружает заранее подготовленный код для проверки парсера.<br>
                    <b>Список литературы</b> — выводит перечень использованных источников.<br>
                    <b>Исходный код программы</b> — открывает листинг кода самого приложения.<br>
                </div>
                <p align='center'><img src='images/help/menu_text.jpg' width='450'></p>

                <h2 style='color: black; font-size: 20px;'>Меню "Пуск"</h2>
                <div style='margin-left: 20px;'>
                    <b>Запуск синтаксического анализатора</b> — инициирует проверку кода в активной вкладке. Выполняет лексический и синтаксический анализ с выводом результатов в таблицу.<br>
                </div>
                <p align='center'><img src='images/help/menu_run.jpg' width='450'></p>

                <h2 style='color: black; font-size: 20px;'>Меню "Справка"</h2>
                <div style='margin-left: 20px;'>
                    <b>Вызов справки</b> — открывает данное руководство пользователя.<br>
                    <b>О программе</b> — выводит информацию о разработчике, теме работы и версии приложения.<br>
                </div>
                <p align='center'><img src='images/help/menu_help.jpg' width='450'></p>

                <h2 style='color: black; font-size: 20px;'>Панель инструментов</h2>
                <p>Для быстрого доступа к основным операциям предусмотрена панель под главным меню:</p>
                <div style='margin-left: 20px;'>
                    На панели расположены кнопки: Создать, Открыть, Сохранить, Отменить, Повторить, Копировать, Вырезать, Вставить, Запуск анализатора и Вызов справки. Также присутствует инструмент для быстрого <b>изменения масштаба шрифта</b> в редакторе.<br>
                </div>
                <p align='center'><img src='images/help/toolbar.jpg' width='450'></p>

                <h2 style='color: black; font-size: 20px;'>Рабочая область и обработка ошибок</h2>
                <div style='margin-left: 20px;'>
                    <b>Многовкладочный интерфейс</b> — позволяет открывать и редактировать несколько файлов одновременно.<br>
                    <b>Редактор кода</b> — поддерживает автоматическую нумерацию строк и подсветку синтаксиса (синий для ключевых слов, зеленый для строк, серый для комментариев и оранжевый для чисел).<br>
                    <b>Таблица результатов</b> — отображает найденные в ходе анализа ошибки. Содержит столбцы: №, Местоположение (строка, символ), Описание ошибки и Неверный фрагмент. Система настроена на строгую локализацию: одна фактическая ошибка генерирует ровно одно точное сообщение в таблице.<br>
                </div>
                <p align='center'><img src='images/help/workspace.jpg' width='450'></p>
            </body>
            </html>
            """,
            "en": """
            <html>
            <body style='font-family: Arial, sans-serif; font-size: 18px; line-height: 1.6; padding: 20px; color: black;'>
                <h1 style='color: black; border-bottom: 2px solid black; font-size: 24px;'>Program Functions Description</h1>

                <p>Main program window with workspace and results table:</p>
                <p align='center'><img src='images/help/main_window.jpg' width='450'></p>

                <h2 style='color: black; font-size: 20px;'> "File" Menu</h2>
                <div style='margin-left: 20px;'>
                    <b>Create</b> — creates a new document and opens it in a new tab.<br>
                    <b>Open</b> — loads text from a selected file.<br>
                    <b>Save</b> — saves current changes to the active file.<br>
                    <b>Save As</b> — allows saving the document under a new name.<br>
                    <b>Exit</b> — closes the application (with a prompt to save changes).<br>
                </div>
                <p align='center'><img src='images/help/menu_file.jpg' width='450'></p>

                <h2 style='color: black; font-size: 20px;'> "Edit" Menu</h2>
                <div style='margin-left: 20px;'>
                    <b>Undo</b> — reverts text to the state before the last change.<br>
                    <b>Redo</b> — cancels the 'Undo' action.<br>
                    <b>Cut</b> — removes selected text and places it in the clipboard.<br>
                    <b>Copy</b> — copies selected text to the clipboard.<br>
                    <b>Paste</b> — inserts text from the clipboard.<br>
                    <b>Delete</b> — clears the selected text fragment.<br>
                    <b>Select All</b> — highlights all text in the current editing window.<br>
                </div>
                <p align='center'><img src='images/help/menu_edit.jpg' width='450'></p>

                <h2 style='color: black; font-size: 20px;'> "Text" Menu</h2>
                <div style='margin-left: 20px;'>
                    <b>Task Formulation</b> — opens a window with the course project assignment description.<br>
                    <b>Grammar</b> — displays grammar rules for Swift language lambda expressions.<br>
                    <b>Grammar Classification</b> — provides info about the grammar type used.<br>
                    <b>Analysis Method</b> — describes the parser's algorithm logic.<br>
                    <b>Diagnostics and Error Neutralization</b> — details the error detection mechanism.<br>
                    <b>Test Example</b> — loads predefined code to verify the parser.<br>
                    <b>References</b> — displays the list of used sources.<br>
                    <b>Program Source Code</b> — opens the listing of the application's own code.<br>
                </div>
                <p align='center'><img src='images/help/menu_text.jpg' width='450'></p>

                <h2 style='color: black; font-size: 20px;'> "Run" Menu</h2>
                <div style='margin-left: 20px;'>
                    <b>Run Parser</b> — initiates the analysis of the code in the active tab. Performs lexical and syntax analysis with results output to the table.<br>
                </div>
                <p align='center'><img src='images/help/menu_run.jpg' width='450'></p>

                <h2 style='color: black; font-size: 20px;'> "Help" Menu</h2>
                <div style='margin-left: 20px;'>
                    <b>View Help</b> — opens this user manual.<br>
                    <b>About</b> — displays developer info, project theme, and version.<br>
                </div>
                <p align='center'><img src='images/help/menu_help.jpg' width='450'></p>

                <h2 style='color: black; font-size: 20px;'>Toolbar</h2>
                <p>For quick access to core operations, a toolbar is provided below the main menu:</p>
                <div style='margin-left: 20px;'>
                    The panel includes buttons for: Create, Open, Save, Undo, Redo, Copy, Cut, Paste, Run Parser, and View Help. A <b>Font Zoom</b> tool is also available for quick adjustment of the editor text size.<br>
                </div>
                <p align='center'><img src='images/help/toolbar.jpg' width='450'></p>

                <h2 style='color: black; font-size: 20px;'>Workspace and Error Handling</h2>
                <div style='margin-left: 20px;'>
                    <b>Multi-tab Interface</b> — allows opening and editing several files simultaneously.<br>
                    <b>Code Editor</b> — supports automatic line numbering and syntax highlighting (Blue for keywords, Green for strings, Gray for comments, and Orange for numbers).<br>
                    <b>Results Table</b> — displays errors found during analysis. Columns include: No., Location (line, char), Error Description, and Invalid Fragment. The system is tuned for strict localization: one actual error generates exactly one precise message in the table.<br>
                </div>
                <p align='center'><img src='images/help/workspace.jpg' width='450'></p>
            </body>
            </html>
            """
        }
        self.browser.setHtml(help_content.get(lang, help_content["ru"]))
        layout.addWidget(self.browser)