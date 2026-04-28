import os
import webbrowser
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import Qt
from help_window import HelpWindow
from translations import STRINGS
from PyQt6.QtGui import QTextCursor, QColor
from scanner import Scanner
from parser import Parser
from antlr4.error.ErrorListener import ErrorListener
from antlr4 import InputStream, CommonTokenStream
from antlr_tool.MyGrammarLexer import MyGrammarLexer
from antlr_tool.MyGrammarParser import MyGrammarParser
from info_windows import DocWindow

class MyAntlrErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        symbol_text = offendingSymbol.text if offendingSymbol else ""
        if not symbol_text and "at: '" in msg:
            symbol_text = msg.split("'")[1]

        error_info = {
            "line": line,
            "column": column,
            "message": msg,
            "symbol": symbol_text or "<EOF>"
        }
        self.errors.append(error_info)


class EditorController:
    def __init__(self, main_window):
        self.ui = main_window
        self.lang = "ru"

    def run_antlr_analysis(self):
        editor = self.ui.get_current_editor()
        if not editor: return

        table = self.ui.output_panel.output_table
        table.setRowCount(0)

        file_path = editor.property("file_path") or "New File"
        text = editor.toPlainText()
        input_stream = InputStream(text)

        lexer = MyGrammarLexer(input_stream)
        lexer.removeErrorListeners()
        stream = CommonTokenStream(lexer)

        parser = MyGrammarParser(stream)
        parser.removeErrorListeners()

        error_listener = MyAntlrErrorListener()
        lexer.addErrorListener(error_listener)
        parser.addErrorListener(error_listener)

        try:
            parser.startRule()
        except Exception as e:
            print(f"Критическая ошибка ANTLR: {e}")

        if not error_listener.errors:
            self.ui.statusBar().showMessage("ANTLR: Ошибок не обнаружено", 5000)
            return

        for i, err in enumerate(error_listener.errors, start=1):
            row = table.rowCount()
            table.insertRow(row)

            items = [
                QTableWidgetItem(str(i)),
                QTableWidgetItem(file_path),
                QTableWidgetItem(err["symbol"] if err["symbol"] else "<WS/EOF>"),
                QTableWidgetItem(err["message"]),
                QTableWidgetItem(f"{err['line']}:{err['column']}")
            ]

            items[4].setData(Qt.ItemDataRole.UserRole, (err["line"], err["column"], len(err["symbol"]) or 1))

            for item in items:
                item.setBackground(QColor("#FFCCCC"))
                table.setItem(row, items.index(item), item)

        self.ui.statusBar().showMessage(f"ANTLR: Найдено ошибок: {len(error_listener.errors)}", 5000)

    def file_new(self):
        title = STRINGS[self.lang]["action_new"]
        self.ui.add_new_tab(title=title)
        self.ui.statusBar().showMessage(STRINGS[self.lang]["msg_new_file"], 5000)

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
            idx = self.ui.tabs.indexOf(editor)
            self.ui.tabs.setTabText(idx, os.path.basename(path))
            self.ui.tabs.setTabToolTip(idx, path)
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
        title = STRINGS[self.lang].get("action_about", "О программе")

        if self.lang == "en":
            msg = (
                "<h3>Language Processor</h2>"
                "<p><b>Version:</b> 1.0.0</p>"
                "<p><b>Author:</b> Violetta Izhboldina (Group AVT-313)</p>"
                "<p>This program is designed for syntax analysis of <b>Swift Lambda expressions</b> "
                "using the Irons method for error neutralization.</p>"
                "<p><i>Functionality:</i> Multi-tab editor, lexical and syntax analysis.</p>"
            )
        else:
            msg = (
                "<h3>Языковой процессор</h2>"
                "<p><b>Версия:</b> 1.0.0</p>"
                "<p><b>Автор:</b> Ижболдина Виолетта (гр. АВТ-313)</p>"
                "<p>Программа предназначена для синтаксического анализа <b>лямбда-выражений Swift</b> "
                "с использованием метода Айронса для нейтрализации ошибок."
                "<p>Функционал:</i> многовкладочный редактор, лексический и синтаксический анализ.</p>"
            )

        QMessageBox.about(self.ui, title, msg)

    def show_document(self, doc_type):
        docs_filenames = {
            "task": "task.html",
            "grammar": "grammar.html",
            "classification": "classification.html",
            "method": "method.html",
            "test_case": "test_case.html",
            "references": "references.html",
            "source_code": "source_code.html",
            "help": "help.html",
        }
        if doc_type in docs_filenames:
            filename = docs_filenames[doc_type]
            current_lang = self.ui.current_lang

            rel_path = os.path.join("docs", current_lang, filename)
            abs_path = os.path.abspath(rel_path)

            if os.path.exists(abs_path):
                webbrowser.open(f"file://{abs_path}")
            else:
                msg = "File not found" if current_lang == "en" else "Файл не найден"
                QMessageBox.warning(self.ui, "Error" if current_lang == "en" else "Ошибка", f"{msg}: {rel_path}")

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

    def run_lexer(self):
        editor = self.ui.get_current_editor()
        if not editor: return

        file_path = editor.property("file_path") or "New File"
        text = editor.toPlainText()

        scanner = Scanner()
        tokens = scanner.analyze(text)
        parser = Parser(tokens)
        syntax_errors = parser.parse()

        table = self.ui.output_panel.output_table
        table.setRowCount(0)

        if not syntax_errors:
            self.ui.statusBar().showMessage(STRINGS[self.lang]["msg_no_errors"], 5000)
            return

        for i, err in enumerate(syntax_errors, start=1):
            row = table.rowCount()
            table.insertRow(row)

            fragment = err.token.lexeme if err.token else "EOF"
            pos_str = f"({err.token.line}, {err.token.start})" if err.token else "-"

            description = err.message

            items = [
                QTableWidgetItem(str(i)),
                QTableWidgetItem(file_path),
                QTableWidgetItem(fragment),
                QTableWidgetItem(description),
                QTableWidgetItem(pos_str)
            ]

            if err.token:
                length = err.token.end - err.token.start + 1
                items[4].setData(Qt.ItemDataRole.UserRole, (err.token.line, err.token.start, length))

            for col, item in enumerate(items):
                item.setBackground(QColor("#ffcccc"))
                table.setItem(row, col, item)

        msg = STRINGS[self.lang]["msg_errors_found"].format(len(syntax_errors))
        self.ui.statusBar().showMessage(msg, 5000)

    def _add_token_to_table(self, table, error, index):
        row = table.rowCount()
        table.insertRow(row)

        item_id = QTableWidgetItem(str(index))
        item_msg = QTableWidgetItem(error.message)
        item_lex = QTableWidgetItem(error.lexeme if error.lexeme else "—")
        item_pos = QTableWidgetItem(f"{error.line}:{error.column}")

        lex_len = len(error.lexeme) if error.lexeme else 1
        item_pos.setData(Qt.ItemDataRole.UserRole, (error.line, error.column, lex_len))

        for item in [item_id, item_msg, item_lex, item_pos]:
            item.setBackground(QColor("#FFCCCC"))

        table.setItem(row, 0, item_id)
        table.setItem(row, 1, item_msg)
        table.setItem(row, 2, item_lex)
        table.setItem(row, 3, item_pos)

    def on_table_item_clicked(self, table, row):
        pos_item = table.item(row, table.columnCount() - 1)
        if not pos_item: return

        data = pos_item.data(Qt.ItemDataRole.UserRole)
        if not data: return

        line, start_col, length = data
        editor = self.ui.get_current_editor()
        if editor:
            cursor = editor.textCursor()
            block = editor.document().findBlockByNumber(line - 1)
            new_pos = block.position() + (start_col - 1)
            cursor.setPosition(new_pos)
            cursor.movePosition(
                QTextCursor.MoveOperation.Right,
                QTextCursor.MoveMode.KeepAnchor,
                length
            )
            editor.setTextCursor(cursor)
            editor.setFocus()