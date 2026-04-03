from PyQt6.QtWidgets import QTabWidget, QTableWidget, QHeaderView
from translations import STRINGS

class OutputPanel(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.output_table = self._create_table(5)
        self.rv_table = self._create_table(5)

        self.addTab(self.output_table, "Вывод")
        self.addTab(self.rv_table, "РВ")
        self.retranslate("ru")

    def _create_table(self, column_count):
        table = QTableWidget()
        table.setColumnCount(column_count)
        table.verticalHeader().setVisible(False)
        header = table.horizontalHeader()

        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        return table

    def retranslate(self, lang):
        s = STRINGS[lang]
        self.setTabText(0, s.get("tab_lexer", "Вывод"))
        self.setTabText(1, s.get("tab_regex", "РВ"))

        self.rv_table.setHorizontalHeaderLabels([
            s.get("col_id", "№"),
            s.get("col_path", "Путь к файлу"),
            s.get("col_match", "Найденная подстрока"),
            s.get("col_pos", "Позиция"),
            s.get("col_len", "Длина")
        ])

        headers = [
            s.get("col_id", "№"),
            s.get("col_path", "Путь к файлу"),
            s.get("col_wrong_fragment", "Неверный фрагмент"),
            s.get("col_description", "Описание ошибки"),
            s.get("col_pos", "Местоположение")
        ]
        self.output_table.setHorizontalHeaderLabels(headers)