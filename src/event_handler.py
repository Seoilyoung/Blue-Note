# 이벤트 처리 / 주요 로직

import sys
from PyQt6.QtWidgets import QApplication
from src.ui_setup import MainWindow

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())