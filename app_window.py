from PyQt6.QtWidgets import QMainWindow, QSplitter, QStatusBar, QLabel, QTabWidget, QToolBar
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from editor_widget import CodeEditorWidget
from output_widget import OutputPanel
from controller import EditorController
from action_manager import ActionManager
from highlighter import PythonHighlighter
from translations import STRINGS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_lang = "ru"
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
        self.retranslate_ui()

    def retranslate_ui(self):
        s = STRINGS[self.current_lang]
        self.setWindowTitle(s["window_title"])
        self.controller.lang = self.current_lang

        self.menu_file.setTitle(s["menu_file"])
        self.menu_edit.setTitle(s["menu_edit"])
        self.menu_text.setTitle(s["menu_text"])
        self.menu_help_top.setTitle(s["menu_help"])
        self.menu_lang.setTitle(s["menu_lang"])

        for i in range(self.tabs.count()):
            editor = self.tabs.widget(i)
            path = editor.property("file_path")
            if not path:
                title = s["action_new"]
                if editor.document().isModified():
                    title += "*"
                self.tabs.setTabText(i, title)

        self.actions.retranslate_actions(self.current_lang)
        self.output_panel.retranslate(self.current_lang)
        self.update_cursor_info()

    def change_language(self, lang_code):
        self.current_lang = lang_code
        self.retranslate_ui()

    def setup_menu(self):
        menu = self.menuBar()
        self.menu_file = menu.addMenu("")
        self.menu_file.addActions(
            [self.actions.menu_new, self.actions.menu_open, self.actions.menu_save, self.actions.menu_save_as,
             self.actions.menu_exit])

        self.menu_edit = menu.addMenu("")
        self.menu_edit.addActions(
            [self.actions.menu_undo, self.actions.menu_redo, self.actions.menu_cut, self.actions.menu_copy,
             self.actions.menu_paste, self.actions.menu_delete, self.actions.menu_select_all])

        self.menu_text = menu.addMenu("")
        menu.addAction(self.actions.menu_run_act)

        self.menu_lang = menu.addMenu("")
        act_ru = self.menu_lang.addAction("Русский")
        act_en = self.menu_lang.addAction("English")
        act_ru.triggered.connect(lambda: self.change_language("ru"))
        act_en.triggered.connect(lambda: self.change_language("en"))

        self.menu_help_top = menu.addMenu("")
        self.menu_help_top.addActions([self.actions.menu_help, self.actions.menu_about])

    def add_new_tab(self, content="", title=None, file_path=None):
        if title is None:
            title = STRINGS[self.current_lang]["action_new"]

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
            if self.tabs.count() == 0: self.add_new_tab()

    def setup_status_bar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.cursor_label = QLabel("")
        self.font_label = QLabel("")
        self.status.addPermanentWidget(self.font_label)
        self.status.addPermanentWidget(self.cursor_label)

    def update_cursor_info(self):
        editor = self.get_current_editor()
        s = STRINGS[self.current_lang]
        if editor:
            cursor = editor.textCursor()
            self.cursor_label.setText(
                f"{s['status_line']}: {cursor.blockNumber() + 1}, {s['status_col']}: {cursor.columnNumber() + 1}")
            self.font_label.setText(f"{s['status_font']}: {editor.font().pointSize()}pt")

    def setup_toolbar(self):
        toolbar = QToolBar("Toolbar")
        toolbar.setIconSize(QSize(28, 28))
        self.addToolBar(toolbar)
        toolbar.addActions([self.actions.new_act, self.actions.open_act, self.actions.save_act])
        toolbar.addSeparator()
        toolbar.addActions([self.actions.undo_act, self.actions.redo_act])
        toolbar.addSeparator()
        toolbar.addActions([self.actions.copy_act, self.actions.cut_act, self.actions.paste_act])
        toolbar.addSeparator()
        toolbar.addAction(self.actions.run_act)
        toolbar.addActions([self.actions.zoom_in_act, self.actions.zoom_out_act])

    def closeEvent(self, event):
        if self.controller.maybe_save_all():
            event.accept()
        else:
            event.ignore()