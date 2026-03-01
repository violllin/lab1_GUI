from PyQt6.QtWidgets import QMainWindow, QSplitter, QStatusBar, QLabel, QTabWidget, QToolBar
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from editor_widget import CodeEditorWidget
from output_widget import OutputPanel
from controller import EditorController
from action_manager import ActionManager
from highlighter import PythonHighlighter
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Текстовый редактор")
        self.resize(1000, 750)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_cursor_info)

        self.output_panel = OutputPanel()

        self.splitter = QSplitter(Qt.Orientation.Vertical)
        self.splitter.addWidget(self.tabs)
        self.splitter.addWidget(self.output_panel)
        self.splitter.setSizes([500, 200])
        self.setCentralWidget(self.splitter)

        self.controller = EditorController(self)
        self.actions = ActionManager(self, self.controller)

        self.setup_menu()
        self.setup_toolbar()
        self.setup_status_bar()

        self.add_new_tab()
        self.setAcceptDrops(True)

    def add_new_tab(self, content="", title="Новый файл", file_path=None):
        editor = CodeEditorWidget()
        editor.setFont(QFont("Courier New", 11))
        editor.setPlainText(content)
        editor.setProperty("file_path", file_path)
        editor.highlighter = PythonHighlighter(editor.document())

        editor.document().modificationChanged.connect(lambda: self.update_tab_title(editor))
        editor.cursorPositionChanged.connect(self.update_cursor_info)

        index = self.tabs.addTab(editor, title)
        self.tabs.setCurrentIndex(index)
        return editor

    def get_current_editor(self):
        return self.tabs.currentWidget()

    def update_tab_title(self, editor):
        index = self.tabs.indexOf(editor)
        if index != -1:
            title = self.tabs.tabText(index).rstrip('*')
            if editor.document().isModified():
                self.tabs.setTabText(index, title + "*")
            else:
                self.tabs.setTabText(index, title)

    def close_tab(self, index):
        if self.controller.maybe_save_tab(index):
            self.tabs.removeTab(index)
            if self.tabs.count() == 0:
                self.add_new_tab()

    def setup_status_bar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.cursor_label = QLabel("Стр: 1, Стлб: 1")
        self.font_label = QLabel("Шрифт: 11pt")
        self.status.addPermanentWidget(self.font_label)
        self.status.addPermanentWidget(self.cursor_label)

    def update_cursor_info(self):
        editor = self.get_current_editor()
        if editor:
            cursor = editor.textCursor()
            line = cursor.blockNumber() + 1
            col = cursor.columnNumber() + 1
            self.cursor_label.setText(f"Стр: {line}, Стлб: {col}")
            self.font_label.setText(f"Шрифт: {editor.font().pointSize()}pt")

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
        edit_m.addAction("Выделить все",
                         lambda: self.get_current_editor().selectAll() if self.get_current_editor() else None)

        text_m = menu.addMenu("Текст")
        for item in ["Постановка задачи", "Грамматика", "Метод анализа", "Тестовый пример", "Список литературы",
                     "Исходный код"]:
            text_m.addAction(item)

        menu.addAction(self.actions.menu_run_act)

        help_m = menu.addMenu("Справка")
        help_m.addActions([self.actions.menu_help, self.actions.menu_about])

    def setup_toolbar(self):
        toolbar = QToolBar("Панель инструментов")
        toolbar.setIconSize(QSize(28, 28))
        self.addToolBar(toolbar)
        toolbar.addActions([self.actions.new_act, self.actions.open_act, self.actions.save_act])
        toolbar.addActions([self.actions.undo_act, self.actions.redo_act])
        toolbar.addActions([self.actions.copy_act, self.actions.cut_act, self.actions.paste_act])
        toolbar.addAction(self.actions.run_act)
        toolbar.addActions([self.actions.zoom_in_act, self.actions.zoom_out_act])

    def closeEvent(self, event):
        if self.controller.maybe_save_all():
            event.accept()
        else:
            event.ignore()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            self.controller.load_file(url.toLocalFile())