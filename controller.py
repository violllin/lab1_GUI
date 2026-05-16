import os
from semantic import SemanticAnalyzer
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
from ir_compiler import TACGenerator, TACOptimizer


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
            except:
                return False
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

    def run_lexer(self):
        editor = self.ui.get_current_editor()
        if not editor:
            return

        file_path = editor.property("file_path") or "New File"
        text = editor.toPlainText()

        scanner = Scanner()
        tokens = scanner.analyze(text)
        parser = Parser(tokens)

        syntax_errors, ast_root = parser.parse()

        self.current_ast = ast_root

        semantic_errors = []
        if ast_root:
            analyzer = SemanticAnalyzer()
            semantic_errors = analyzer.analyze(ast_root)

        all_errors = syntax_errors + semantic_errors

        ast_display = self.ui.output_panel.ast_display
        ast_display.clear()

        if not all_errors and ast_root:
            ast_text = ast_root.to_string()
            ast_display.setPlainText(ast_text)

        table = self.ui.output_panel.output_table
        table.setRowCount(0)

        if not all_errors:
            self.ui.statusBar().showMessage(STRINGS[self.lang]["msg_no_errors"], 5000)

            if self.current_ast:
                try:
                    generator = TACGenerator()
                    raw_ir = generator.generate(self.current_ast)

                    folded_ir, cf_count = TACOptimizer.fold_constants(raw_ir)
                    final_ir, dce_count = TACOptimizer.eliminate_dead_code(folded_ir)

                    calc_result = TACOptimizer.get_final_result(final_ir)

                    report = "ИСХОДНЫЙ ТРЕХАДРЕСНЫЙ КОД\n"
                    report += "\n".join([f"{i + 1}: {line}" for i, line in enumerate(raw_ir)])

                    report += f"\n\nОПТИМИЗАЦИЯ 1: СВЕРТКА КОНСТАНТ\n"
                    report += f"Применено оптимизаций: {cf_count}\n\n"
                    report += "\n".join([f"{i + 1}: {line}" for i, line in enumerate(folded_ir)])

                    report += f"\n\nОПТИМИЗАЦИЯ 2: УДАЛЕНИЕ МЕРТВОГО КОДА\n"
                    report += f"Удалено инструкций: {dce_count}\n\n"
                    report += "\n".join([f"{i + 1}: {line}" for i, line in enumerate(final_ir)])

                    report += "\n\nИТОГОВЫЙ РЕЗУЛЬТАТ\n"
                    report += f"Всего оптимизаций применено: {cf_count + dce_count}\n"
                    report += f"Размер кода: {len(final_ir)} инструкций\n"
                    report += f"Результат вычисления = {calc_result}"

                    self.ui.output_panel.tac_display.setPlainText(report)

                except Exception as e:
                    self.ui.output_panel.tac_display.setPlainText(f"Ошибка генерации IR: {str(e)}")
            return

        for i, err in enumerate(all_errors, start=1):
            row = table.rowCount()
            table.insertRow(row)

            is_semantic = hasattr(err, 'message') and "Семантич" in err.message
            token = err.token

            fragment = token.lexeme if token else "EOF"
            pos_str = f"({token.line}, {token.start})" if token else "-"
            description = err.message

            items = [
                QTableWidgetItem(str(i)),
                QTableWidgetItem(file_path),
                QTableWidgetItem(fragment),
                QTableWidgetItem(description),
                QTableWidgetItem(pos_str)
            ]

            if token:
                length = token.end - token.start + 1
                items[4].setData(Qt.ItemDataRole.UserRole, (token.line, token.start, length))

            for col, item in enumerate(items):
                bg_color = "#FFE8B2" if is_semantic else "#ffcccc"
                item.setBackground(QColor(bg_color))
                table.setItem(row, col, item)

        msg = STRINGS[self.lang]["msg_errors_found"].format(len(all_errors))
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
        pos_item = None
        for col in range(table.columnCount()):
            item = table.item(row, col)
            if item and item.data(Qt.ItemDataRole.UserRole):
                pos_item = item
                break

        if not pos_item: return

        line, start_col, length = pos_item.data(Qt.ItemDataRole.UserRole)
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

    def show_ast_visualizer(self):
        if not hasattr(self, 'current_ast') or self.current_ast is None:
            QMessageBox.warning(self.ui, "Внимание", "Сначала выполните анализ кода.")
            return

        from ast_visualizer import ASTVisualizer
        dialog = ASTVisualizer(self.current_ast, self.ui)
        dialog.exec()