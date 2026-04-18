from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser


class DocWindow(QDialog):
    def __init__(self, title, file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(800, 600)

        layout = QVBoxLayout(self)

        self.browser = QTextBrowser()
        layout.addWidget(self.browser)

        self.load_content(file_path)

    def load_content(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                html_content = f.read()
                self.browser.setHtml(html_content)
        except Exception as e:
            self.browser.setHtml(f"<h1>Ошибка</h1><p>Не удалось загрузить файл: {path}</p><p>{str(e)}</p>")