from PyQt6.QtWidgets import QMainWindow, QTextEdit, QSplitter, QToolBar, QStatusBar
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from actions import AppActions


class CompilerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI")
        self.resize(900, 700)

        self.actions = AppActions(self)

        self.setup_text_areas()

        self.setup_menu()
        self.setup_toolbar()
        self.setStatusBar(QStatusBar(self))

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

    def setup_menu(self):
        menu = self.menuBar()

        file_m = menu.addMenu("Файл")
        file_m.addActions(
            [self.actions.new_act, self.actions.open_act, self.actions.save_act, self.actions.save_as_act])
        file_m.addSeparator()
        file_m.addAction(self.actions.exit_act)

        edit_m = menu.addMenu("Правка")
        edit_m.addActions([self.actions.undo_act, self.actions.redo_act])
        edit_m.addSeparator()
        edit_m.addActions([self.actions.cut_act, self.actions.copy_act, self.actions.paste_act])

        text_m = menu.addMenu("Текст")
        for item in ["Постановка задачи", "Грамматика", "Классификация грамматики", "Метод анализа"]:
            text_m.addAction(item)

        run_m = menu.addMenu("Пуск")

        help_m = menu.addMenu("Справка")
        help_m.addAction(self.actions.help_act)
        help_m.addAction(self.actions.about_act)

    def setup_toolbar(self):
        toolbar = QToolBar("Панель инструментов")
        toolbar.setIconSize(QSize(28, 28))
        self.addToolBar(toolbar)

        toolbar.addAction(self.actions.new_act)
        toolbar.addAction(self.actions.open_act)
        toolbar.addAction(self.actions.save_act)
        toolbar.addSeparator()
        toolbar.addAction(self.actions.undo_act)
        toolbar.addAction(self.actions.redo_act)
        toolbar.addSeparator()
        toolbar.addAction(self.actions.copy_act)
        toolbar.addAction(self.actions.cut_act)
        toolbar.addAction(self.actions.paste_act)
        toolbar.addSeparator()
        toolbar.addAction(self.actions.run_act)
        toolbar.addSeparator()
        toolbar.addAction(self.actions.help_act)
        toolbar.addAction(self.actions.about_act)