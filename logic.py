from PyQt6.QtWidgets import QFileDialog, QMessageBox
from help_window import HelpWindow

class EditorLogic:
    def __init__(self, ui_window):
        self.ui = ui_window
        self.current_path = None

    def file_new(self):
        if self.maybe_save():
            self.ui.editor.clear()
            self.current_path = None
            self.ui.editor.document().setModified(False)

    def file_open(self):
        if self.maybe_save():
            path, _ = QFileDialog.getOpenFileName(self.ui, "Открыть файл", "", "Text Files (*.txt);;All Files (*)")
            if path:
                with open(path, 'r', encoding='utf-8') as f:
                    self.ui.editor.setPlainText(f.read())
                self.current_path = path
                self.ui.editor.document().setModified(False)

    def file_save(self):
        if self.current_path:
            with open(self.current_path, 'w', encoding='utf-8') as f:
                f.write(self.ui.editor.toPlainText())
            self.ui.editor.document().setModified(False)
            return True
        else:
            return self.file_save_as()

    def file_save_as(self):
        path, _ = QFileDialog.getSaveFileName(self.ui, "Сохранить как", "", "Text Files (*.txt);;All Files (*)")
        if path:
            self.current_path = path
            return self.file_save()
        return False

    def maybe_save(self):
        if not self.ui.editor.document().isModified():
            return True

        ret = QMessageBox.question(self.ui, "Сохранить изменения?",
                                   "В документе есть изменения. Сохранить их?",
                                   QMessageBox.StandardButton.Save |
                                   QMessageBox.StandardButton.Discard |
                                   QMessageBox.StandardButton.Cancel)

        if ret == QMessageBox.StandardButton.Save:
            return self.file_save()
        elif ret == QMessageBox.StandardButton.Cancel:
            return False
        return True

    def show_about(self):
        about_text = (
            "Текстовый редактор\n\n"
            "Реализован функционал меню 'Справка' и 'Правка'"
        )
        QMessageBox.information(self.ui, "О программе", about_text)

    def show_help(self):
        self.help_dialog = HelpWindow(self.ui)
        self.help_dialog.show()