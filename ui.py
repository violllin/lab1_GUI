from PyQt6.QtWidgets import QMainWindow, QTextEdit, QSplitter, QToolBar, QStatusBar, QLabel
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from actions import AppActions
from logic import EditorLogic


class CompilerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Текстовый редактор")
        self.resize(900, 700)

        self.setup_text_areas()

        self.logic = EditorLogic(self)
        self.actions = AppActions(self, self.logic)

        self.setup_menu()
        self.setup_toolbar()
        self.setup_status_bar()

        self.editor.document().modificationChanged.connect(self.setWindowModified)
        self.editor.cursorPositionChanged.connect(self.update_cursor_info)

        self.setAcceptDrops(True)
        self.editor.setAcceptDrops(False)

    def setup_text_areas(self):
        self.splitter = QSplitter(Qt.Orientation.Vertical)
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Courier New", 11))
        self.results = QTextEdit()
        self.results.setReadOnly(True)
        self.results.setFont(QFont("Courier New", 11))
        self.splitter.addWidget(self.editor)
        self.splitter.addWidget(self.results)
        self.splitter.setSizes([500, 200])
        self.setCentralWidget(self.splitter)

    def setup_status_bar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.cursor_label = QLabel("Стр: 1, Стлб: 1")
        self.status.addPermanentWidget(self.cursor_label)

    def update_cursor_info(self):
        cursor = self.editor.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        self.cursor_label.setText(f"Стр: {line}, Стлб: {col}")

    def closeEvent(self, event):
        if self.logic.maybe_save():
            event.accept()
        else:
            event.ignore()

    def setup_menu(self):
        menu = self.menuBar()
        file_m = menu.addMenu("Файл")
        file_m.addActions(
            [self.actions.menu_new, self.actions.menu_open, self.actions.menu_save, self.actions.menu_save_as])
        file_m.addAction(self.actions.menu_exit)

        edit_m = menu.addMenu("Правка")
        edit_m.addActions([self.actions.menu_undo, self.actions.menu_redo])
        edit_m.addActions(
            [self.actions.menu_cut, self.actions.menu_copy, self.actions.menu_paste, self.actions.menu_delete])
        edit_m.addAction("Выделить все", self.editor.selectAll)

        text_m = menu.addMenu("Текст")
        for item in ["Постановка задачи", "Грамматика", "Метод анализа", "Тестовый пример", "Список литературы",
                     "Исходный код программы"]:
            text_m.addAction(item)

        menu.addMenu("Пуск")

        help_m = menu.addMenu("Справка")
        help_m.addActions([self.actions.menu_help, self.actions.menu_about])

    def setup_toolbar(self):
        toolbar = QToolBar("Панель инструментов")
        toolbar.setIconSize(QSize(28, 28))
        self.addToolBar(toolbar)
        toolbar.addActions([self.actions.new_act, self.actions.open_act, self.actions.save_act])
        toolbar.addSeparator()
        toolbar.addActions([self.actions.undo_act, self.actions.redo_act])
        toolbar.addSeparator()
        toolbar.addActions([self.actions.copy_act, self.actions.cut_act, self.actions.paste_act])
        toolbar.addSeparator()
        toolbar.addAction(self.actions.run_act)
        toolbar.addSeparator()
        toolbar.addActions([self.actions.help_act, self.actions.about_act])
        toolbar.addSeparator()
        toolbar.addAction(self.actions.zoom_in_act)
        toolbar.addAction(self.actions.zoom_out_act)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if self.logic.maybe_save():
                self.logic.load_file(file_path)