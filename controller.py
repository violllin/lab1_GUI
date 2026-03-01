import os
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import Qt
from help_window import HelpWindow
from translations import STRINGS

class EditorController:
    def __init__(self, main_window):
        self.ui = main_window
        self.lang = "ru"

    def run_program(self):
        self.ui.output_panel.console_output.clear()
        self.ui.output_panel.errors_output.setRowCount(0)
        editor = self.ui.get_current_editor()
        if not editor: return
        code = editor.toPlainText()
        file_path = editor.property("file_path") or ("Новый файл" if self.lang == "ru" else "New File")
        lines = code.split('\n')
        for i, line_text in enumerate(lines):
            if "error" in line_text.lower():
                self.add_error_to_table(file_path, i + 1, "Ошибка" if self.lang == "ru" else "Error")

    def add_error_to_table(self, path, line, message):
        table = self.ui.output_panel.errors_output
        row = table.rowCount()
        table.insertRow(row)
        items = [QTableWidgetItem(str(row + 1)), QTableWidgetItem(str(path)),
                 QTableWidgetItem(str(line)), QTableWidgetItem(message)]
        items[0].setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        items[2].setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        for col, item in enumerate(items):
            table.setItem(row, col, item)

    def file_new(self):
        title = STRINGS[self.lang]["action_new"]
        self.ui.add_new_tab(title=title)
        self.ui.statusBar().showMessage(STRINGS[self.lang]["msg_new_file"], 3000)

    def file_open(self):
        paths, _ = QFileDialog.getOpenFileNames(self.ui, "Open Files", "", "Text Files (*.txt);;All Files (*)")
        for path in paths:
            if path: self.load_file(path)

    def load_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.ui.add_new_tab(content, os.path.basename(path), path)
        except Exception as e:
            QMessageBox.critical(self.ui, "Error", f"{STRINGS[self.lang]['err_read']}:\n{str(e)}")

    def file_save(self):
        editor = self.ui.get_current_editor()
        if not editor: return False
        path = editor.property("file_path")
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(editor.toPlainText())
                editor.document().setModified(False)
                self.ui.update_tab_title(editor)
                return True
            except: return False
        return self.file_save_as()

    def file_save_as(self):
        editor = self.ui.get_current_editor()
        if not editor: return False
        path, _ = QFileDialog.getSaveFileName(self.ui, "Save As", "", "Text Files (*.txt);;All Files (*)")
        if path:
            editor.setProperty("file_path", path)
            self.ui.tabs.setTabText(self.ui.tabs.indexOf(editor), os.path.basename(path))
            return self.file_save()
        return False

    def maybe_save_tab(self, index):
        editor = self.ui.tabs.widget(index)
        if not editor.document().isModified(): return True
        self.ui.tabs.setCurrentIndex(index)
        s = STRINGS[self.lang]
        ret = QMessageBox.question(self.ui, s["msg_save_change"],
                                   s["msg_save_desc"].format(self.ui.tabs.tabText(index)),
                                   QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)
        if ret == QMessageBox.StandardButton.Save: return self.file_save()
        return ret != QMessageBox.StandardButton.Cancel

    def maybe_save_all(self):
        for i in range(self.ui.tabs.count() - 1, -1, -1):
            if not self.maybe_save_tab(i): return False
        return True

    def show_about(self):
        title = STRINGS[self.lang]["action_about"]
        msg = "Text Editor\nTab functionality implemented" if self.lang == "en" else "Текстовый редактор\nРеализован функционал вкладок"
        QMessageBox.information(self.ui, title, msg)

    def show_help(self):
        self.help_window = HelpWindow(self.ui, self.lang)
        self.help_window.show()

    def zoom_in(self):
        editor = self.ui.get_current_editor()
        if editor:
            font = editor.font()
            font.setPointSize(font.pointSize() + 2)
            editor.setFont(font)
            editor.update_line_number_area_width()
            self.ui.update_cursor_info()

    def zoom_out(self):
        editor = self.ui.get_current_editor()
        if editor:
            font = editor.font()
            new_size = font.pointSize() - 2
            if new_size >= 6:
                font.setPointSize(new_size)
                editor.setFont(font)
                editor.update_line_number_area_width()
                self.ui.update_cursor_info()