from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt

class MyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.table_widget = QTableWidget()
        self.setCentralWidget(self.table_widget)
        self.table_widget.setColumnCount(2)
        self.table_widget.setRowCount(2)
        self.table_widget.cellChanged.connect(self.on_cell_changed)
        
        # 테이블 위젯 초기 값 설정
        for row in range(2):
            for column in range(2):
                item = QTableWidgetItem(f"{row}, {column}")
                self.table_widget.setItem(row, column, item)

    def on_cell_changed(self, row, column):
        print(self)
        item = self.table_widget.item(row, column)
        if item is not None:
            print(f"Cell ({row}, {column}) 값 변경: {item.text()}")
        else:
            print(f"Cell ({row}, {column}) 값 변경: None")
            
if __name__ == '__main__':
    app = QApplication([])
    main_window = MyMainWindow()
    main_window.show()
    app.exec()
