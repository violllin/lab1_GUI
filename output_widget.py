from PyQt6.QtWidgets import QTabWidget, QTableWidget, QHeaderView
from translations import STRINGS


class OutputPanel(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.errors_table = self._create_table(5)
        self.lexer_table = self._create_table(6)
        self.tetrads_table = self._create_table(6)

        self.addTab(self.errors_table, "")
        self.addTab(self.lexer_table, "")
        self.addTab(self.tetrads_table, "")

        self.retranslate("ru")

    def _create_table(self, cols):
        table = QTableWidget()
        table.setColumnCount(cols)
        table.verticalHeader().setVisible(False)
        header = table.horizontalHeader()
        for i in range(cols):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        return table

    def retranslate(self, lang):
        s = STRINGS[lang]

        self.setTabText(0, s.get("tab_errors", "Ошибки"))
        self.setTabText(1, s.get("tab_lexer_result", "Лексер"))
        self.setTabText(2, s.get("tab_tetrads", "Тетрады"))

        self.errors_table.setHorizontalHeaderLabels([
            s.get("col_id", "№"),
            s.get("col_path", "Путь к файлу"),
            s.get("col_wrong_fragment", "Фрагмент"),
            s.get("col_description", "Описание"),
            s.get("col_pos", "Местоположение")
        ])
        self.lexer_table.setHorizontalHeaderLabels([
            s.get("col_id", "№"),
            s.get("col_path", "Путь к файлу"),
            s.get("col_code", "Код"),
            s.get("col_lex_type", "Тип"),
            s.get("col_lex_value", "Значение"),
            s.get("col_pos", "Местоположение")
        ])
        self.tetrads_table.setHorizontalHeaderLabels([
            s.get("col_id", "№"),
            s.get("col_path", "Путь к файлу"),
            s.get("col_operator", "Оператор"),
            s.get("col_operand1", "Операнд 1"),
            s.get("col_operand2", "Операнд 2"),
            s.get("col_result", "Результат")
        ])