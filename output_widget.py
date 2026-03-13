from PyQt6.QtWidgets import QTabWidget, QTableWidget, QHeaderView
from translations import STRINGS
class OutputPanel(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.lexer_table = self._create_table()

        self.errors_table = self._create_table()

        self.addTab(self.lexer_table, "")
        self.addTab(self.errors_table, "")
        self.retranslate("ru")

    def _create_table(self):
        table = QTableWidget()
        table.setColumnCount(6)
        table.verticalHeader().setVisible(False)

        header = table.horizontalHeader()

        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        return table

    def retranslate(self, lang):
        s = STRINGS[lang]
        self.setTabText(0, s.get("tab_lexer", "Вывод"))
        self.setTabText(1, s.get("tab_errors", "Ошибки"))

        headers = [
            s.get("col_id", "№"),
            s.get("col_path", "Путь к файлу"),
            s.get("col_code", "Условный код"),
            s.get("col_type", "Тип лексемы"),
            s.get("col_value", "Значение"),
            s.get("col_pos", "Позиция (строка, символ)")
        ]
        self.lexer_table.setHorizontalHeaderLabels(headers)
        self.errors_table.setHorizontalHeaderLabels(headers)