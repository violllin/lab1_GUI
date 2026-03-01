from PyQt6.QtWidgets import (QMainWindow, QTextEdit, QSplitter, QToolBar, QStatusBar, QLabel, QTabWidget, QPlainTextEdit, QWidget,
                             QTableWidget, QHeaderView, QAbstractItemView)
from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtGui import QFont, QPainter, QColor
from actions import AppActions
from logic import EditorLogic
from highlighter import PythonHighlighter

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor
    def sizeHint(self):
        return QSize(self.codeEditor.line_number_area_width(), 0)
    def paintEvent(self, event):
        self.codeEditor.line_number_area_paint_event(event)

class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.update_line_number_area_width(0)

    def line_number_area_width(self):
        digits = 1
        max_blocks = max(1, self.blockCount())
        while max_blocks >= 10:
            max_blocks //= 10
            digits += 1
        space = 15 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, _=0):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#f0f0f0"))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor("#888888"))
                painter.drawText(0, top, self.line_number_area.width() - 5, self.fontMetrics().height(),
                                 Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            block_number += 1


class CompilerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Текстовый редактор")
        self.resize(1000, 750)

        self.setup_text_areas()

        self.logic = EditorLogic(self)
        self.actions = AppActions(self, self.logic)

        self.setup_menu()
        self.setup_toolbar()
        self.setup_status_bar()

        self.add_new_tab()
        self.setAcceptDrops(True)

    def setup_text_areas(self):
        self.splitter = QSplitter(Qt.Orientation.Vertical)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_cursor_info)

        self.result_tabs = QTabWidget()
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setFont(QFont("Courier New", 11))

        self.errors_output = QTableWidget()
        self.errors_output.setColumnCount(4)
        self.errors_output.setHorizontalHeaderLabels(["№", "Путь к файлу", "Линия", "Сообщение"])

        self.errors_output.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.errors_output.verticalHeader().setVisible(False)

        header = self.errors_output.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.result_tabs.addTab(self.console_output, "Вывод")
        self.result_tabs.addTab(self.errors_output, "Ошибки")

        self.splitter.addWidget(self.tabs)
        self.splitter.addWidget(self.result_tabs)
        self.splitter.setSizes([500, 200])
        self.setCentralWidget(self.splitter)

    def add_new_tab(self, content="", title="Новый файл", file_path=None):
        editor = CodeEditor()
        editor.setFont(QFont("Courier New", 11))
        editor.setPlainText(content)
        editor.setAcceptDrops(False)
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
        if self.logic.maybe_save_tab(index):
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

    def closeEvent(self, event):
        if self.logic.maybe_save_all():
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
        edit_m.addAction("Выделить все",
                         lambda: self.get_current_editor().selectAll() if self.get_current_editor() else None)
        text_m = menu.addMenu("Текст")
        for item in ["Постановка задачи", "Грамматика", "Метод анализа", "Тестовый пример", "Список литературы",
                     "Исходный код программы"]:
            text_m.addAction(item)
        menu.addMenu("Пуск").addAction(self.actions.run_act)
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
        for url in urls:
            file_path = url.toLocalFile()
            self.logic.load_file(file_path)