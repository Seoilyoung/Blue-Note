# 이벤트 처리 / 주요 로직

import sys
from PyQt6.QtWidgets import QApplication
from src.ui_setup import LoadingWindow

def main():
    app = QApplication(sys.argv)
    window = LoadingWindow()
    sys.exit(app.exec())