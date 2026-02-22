from PyQt6.QtWidgets import QMainWindow, QTextEdit, QSplitter, QToolBar, QStatusBar
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
        self.setStatusBar(QStatusBar(self))
        self.editor.document().modificationChanged.connect(self.setWindowModified)

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

    def closeEvent(self, event):
        if self.logic.maybe_save():
            event.accept()
        else:
            event.ignore()

    def setup_menu(self):
        menu = self.menuBar()
        file_m = menu.addMenu("Файл")
        file_m.addActions([self.actions.menu_new, self.actions.menu_open, self.actions.menu_save, self.actions.menu_save_as])
        file_m.addAction(self.actions.menu_exit)

        edit_m = menu.addMenu("Правка")
        edit_m.addActions([self.actions.menu_undo, self.actions.menu_redo])
        edit_m.addActions([self.actions.menu_cut, self.actions.menu_copy, self.actions.menu_paste, self.actions.menu_delete])

        edit_m.addAction("Выделить все", self.editor.selectAll)

        text_m = menu.addMenu("Текст")
        for item in ["Постановка задачи", "Грамматика", "Метод анализа", "Тестовый пример", "Список литературы", "Исходный код программы"]:
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