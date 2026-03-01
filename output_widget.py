from PyQt6.QtWidgets import QTabWidget, QTextEdit, QTableWidget, QHeaderView, QAbstractItemView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from translations import STRINGS

class OutputPanel(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setFont(QFont("Courier New", 11))

        self.errors_output = QTableWidget()
        self.errors_output.setColumnCount(4)
        self.errors_output.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.errors_output.verticalHeader().setVisible(False)

        header = self.errors_output.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.addTab(self.console_output, "")
        self.addTab(self.errors_output, "")
        self.retranslate("ru")

    def retranslate(self, lang):
        s = STRINGS[lang]
        self.setTabText(0, s["tab_output"])
        self.setTabText(1, s["tab_errors"])
        self.errors_output.setHorizontalHeaderLabels([
            s["table_no"], s["table_path"], s["table_line"], s["table_msg"]
        ])