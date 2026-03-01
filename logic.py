import os
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QTextEdit
from help_window import HelpWindow
class EditorLogic:
    def __init__(self, ui_window):
        self.ui = ui_window

    def file_new(self):
        self.ui.add_new_tab()
        self.ui.statusBar().showMessage("Создан новый файл", 3000)

    def file_open(self):
        paths, _ = QFileDialog.getOpenFileNames(self.ui, "Открыть файлы", "", "Text Files (*.txt);;All Files (*)")
        for path in paths:
            if path:
                self.load_file(path)

    def load_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.ui.add_new_tab(content, os.path.basename(path), path)
            self.ui.statusBar().showMessage(f"Файл открыт: {path}", 3000)
        except Exception as e:
            QMessageBox.critical(self.ui, "Ошибка", f"Не удалось прочитать файл:\n{str(e)}")

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
                self.ui.statusBar().showMessage(f"Сохранено: {path}", 3000)
                return True
            except Exception as e:
                self.ui.statusBar().showMessage("Ошибка при сохранении", 5000)
                return False
        else:
            return self.file_save_as()

    def file_save_as(self):
        editor = self.ui.get_current_editor()
        if not editor: return False

        path, _ = QFileDialog.getSaveFileName(self.ui, "Сохранить как", "", "Text Files (*.txt);;All Files (*)")
        if path:
            editor.setProperty("file_path", path)
            self.ui.tabs.setTabText(self.ui.tabs.indexOf(editor), os.path.basename(path))
            return self.file_save()
        return False

    def maybe_save_tab(self, index):
        editor = self.ui.tabs.widget(index)
        if not editor.document().isModified():
            return True

        self.ui.tabs.setCurrentIndex(index)
        ret = QMessageBox.question(self.ui, "Сохранить изменения?",
                                   f"В файле '{self.ui.tabs.tabText(index)}' есть изменения. Сохранить их?",
                                   QMessageBox.StandardButton.Save |
                                   QMessageBox.StandardButton.Discard |
                                   QMessageBox.StandardButton.Cancel)

        if ret == QMessageBox.StandardButton.Save:
            return self.file_save()
        elif ret == QMessageBox.StandardButton.Cancel:
            return False
        return True

    def maybe_save_all(self):
        for i in range(self.ui.tabs.count() - 1, -1, -1):
            if not self.maybe_save_tab(i):
                return False
        return True

    def show_about(self):
        about_text = ("Текстовый редактор\n\nРеализован функционал вкладок и дополнительные функции")
        QMessageBox.information(self.ui, "О программе", about_text)

    def show_help(self):
        self.help_dialog = HelpWindow(self.ui)
        self.help_dialog.show()

    def zoom_in(self):
        editor = self.ui.get_current_editor()
        if editor:
            font = editor.font()
            font.setPointSize(font.pointSize() + 2)
            editor.setFont(font)
            editor.update_line_number_area_width()
            self.ui.update_cursor_info()
            for i in range(self.ui.result_tabs.count()):
                widget = self.ui.result_tabs.widget(i)
                if isinstance(widget, QTextEdit):
                    widget.setFont(font)

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
                for i in range(self.ui.result_tabs.count()):
                    widget = self.ui.result_tabs.widget(i)
                    if isinstance(widget, QTextEdit):
                        widget.setFont(font)