import sys
from PyQt6.QtWidgets import QApplication
from ui import CompilerUI

def main():
    app = QApplication(sys.argv)

    window = CompilerUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()