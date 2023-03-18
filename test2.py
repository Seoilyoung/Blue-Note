from PyQt6.QtWidgets import (QMainWindow, QApplication, QListWidgetItem, QAbstractItemView,
    QTableWidgetItem)
from PyQt6.uic import loadUi
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QSize, Qt, QDataStream, QIODevice

class MyListWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        mainscreen_path = 'Gui\Screen.ui'
        loadUi(mainscreen_path,self)
        # Drag and drop 설정
        self.listWidget_cal1.setDragEnabled(True)
        self.listWidget_cal1.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)

        list_char = ['시로코','아즈사','아루','카즈사','호시노']
        # QListWidgetItem 추가
        for i in range(5):
            img_path = f"Gui/Useimages/'character'/{i+1:02}.webp"
            pixmap = QPixmap(img_path)
            container_ui = loadUi('Gui\Container_char.ui')
            container = QListWidgetItem(self.listWidget_cal1)
            container.setSizeHint(QSize(0,50))
            container_ui.label_img.setContentsMargins(5,5,5,5)
            container_ui.label_img.setPixmap(pixmap)
            for row in range(container_ui.tableWidget_cal.rowCount()):
                for column in range(container_ui.tableWidget_cal.columnCount()):
                     item_value = row+column
                     item = QTableWidgetItem(str(item_value))
                     item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                     container_ui.tableWidget_cal.setItem(row, column, item)

            container_ui.comboBox.setCurrentText(list_char[i])
             
            self.listWidget_cal1.addItem(container)
            self.listWidget_cal1.setItemWidget(container, container_ui)

        # 리스트 위젯에 대한 drop 이벤트 처리 함수 등록
        self.listWidget_cal1.setAcceptDrops(True)
        self.listWidget_cal1.viewport().setAcceptDrops(True)
        
        self.listWidget_cal1.dropEvent = self.dropEvent


    def dropEvent(self, event):
        print("test")
        if event.source() != self.listWidget_cal1:
            
            print("test2")
            super().dropEvent(event)
        else:
            print("test3")
            # 드래그한 아이템의 데이터를 가져와서 이동합니다.
            mimeData = event.mimeData()
            if mimeData.hasFormat("application/x-qabstractitemmodeldatalist"):
                encoded = mimeData.data("application/x-qabstractitemmodeldatalist")
                stream = QDataStream(encoded, QIODevice.OpenModeFlag.ReadOnly)
                row, col, _ = stream.readInt32(), stream.readInt32(), stream.readInt32()
                itemData = stream.readBytes()

                item = self.listWidget_cal1.itemAt(event.position().toPoint())
                if item:
                    # 기존 아이템 위로 드롭한 경우, 그 위로 삽입합니다.
                    self.listWidget_cal1.insertItem(self.listWidget_cal1.row(item), "")
                else:
                    # 리스트 위젯의 끝으로 드롭한 경우, 맨 끝에 삽입합니다.
                    self.listWidget_cal1.addItem("")

                newItem = self.listWidget_cal1.item(self.listWidget_cal1.row(item))
                newItem.setData(Qt.ItemDataRole.UserRole, itemData)
                widget = self.listWidget_cal1.itemWidget(item)
                self.listWidget_cal1.setItemWidget(newItem, widget)

if __name__ == "__main__":
    app = QApplication([])
    mylistwidget = MyListWidget()
    mylistwidget.show()
    app.exec()

