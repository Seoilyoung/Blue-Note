import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QListWidget, QLineEdit
from PyQt6.QtGui import QIcon,QAction,QPixmap, QFont
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        pic = """
            background-image:url(Gui/background.png);
            background-repeat: no-repeat;
            background-position: center;
        """
        # QMainWindow
        self.setWindowTitle('PyQt6 Example')
        self.setStyleSheet(pic)
        self.resize(1280,730)
        # self.setMinimumSize(1280,730)
        # self.setMaximumSize(1280,730)
        # self.setWindowIcon(QIcon("abc/abc.ico"))
        
        # # Font
        # self.font = QFont() 
        # self.font.setFamily("Times nEw roman")
        # self.font.setPointSize(20)

        # # Label
        # widget = QLabel("Hello")
        # font = widget.font()
        # font.setPointSize(30)
        # widget.setFont(font)
        # widget.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        # self.setCentralWidget(widget)

        # ListWidget
        listwidget = QListWidget()
        listwidget.addItems(["list1 list1 list1", "list2 list2 list2", "list3 list3 list3"])
        listwidget.currentItemChanged.connect(self.index_changed)
        listwidget.currentItemChanged.connect(self.text_changed)
        self.setCentralWidget(listwidget)


    def index_changed(self, i):
        print(i.text())
    def text_changed(self, s):
        print(s)

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())