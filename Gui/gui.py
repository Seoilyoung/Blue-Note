import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QToolBar, QStatusBar
from PyQt6.QtGui import QIcon,QAction
from PyQt6.QtCore import Qt

class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()
    
    def init_ui(self):
        self.statusBar().showMessage('Ready')

        self.setGeometry(300,300,320,240)
        self.setWindowTitle('PyQt6 Example')

        label = QLabel("Hello!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)

        toolbar = QToolBar("My Toolbar")
        self.addToolBar(toolbar)

        button_action = QAction("Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addAction(button_action)

        self.show()

    def onMyToolBarButtonClick(self, s):
            print("click", s)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())