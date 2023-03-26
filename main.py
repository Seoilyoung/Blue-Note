# Main 코드
# gui코드가 와야 하나?

# 기능
# - AP 존버 가이드
# 	탬플릿 만들고 함수 쓰면 될듯. 서버 연동도 필요없음. 이미지로 저장, 공유 깔끔하게 되면 좋을듯. 
# - 일정(이벤트, 총력전 등)
# 	이건 수동으로 해야 하는거 아닌가? 달력형식, 목록형식으로 구현.
# - 트위터 / 넥슨 홈페이지 새 글 갱신
# 	크롤링
# - 재화 계산(총 재화, 2~3달 내 재화 등 구분 프리셋)
# 	스프레드시트 이미 구현한 것 이용
# - 인게임 연동도 가능한가?(AP, 카페, 숙제, 순위 확인)
# 	api 알아내려면 클뜯을 하면 나오나?
# - 원스 출석 알리미 / 알림이 아니라 출석을 해주거나 출석을 안했을 때 푸시알림
#   이것도 12시에 알리미는 프로그램 알림 기능을 사용하면 가능하겠지만 출석을 하지 않았을 때를 파악하려면 어떻게 해야 하나?
# - 총력전 / 이벤트 조력자 매크로
# 	다른 방식으로 이미 구현한 것 이용
# - GUI
#   깔끔하게 원신 구동기 화면
#   종류가 많음. 메모리 먹는거 확인하면서 선택.
# - 트위치 스트리머 확인
#   특정 스트리머 방송 켰는지 확인
# - 함수들 각 py파일로 이동할 수 있으면 옮기자. main이 더럽다

# - 이미지 출처 : 블루 아카이브 디지털 굿즈샵 (https://forum.nexon.com/bluearchive/board_view?thread=1881343)
#                블루아카이브 - 나무위키

import sys
import os
import subprocess
import webbrowser
import asyncio
import atexit

from PyQt6.QtCore import QDate, QTimer, Qt, QUrl, QSize, QPoint, QEvent
from PyQt6.QtGui import QPixmap, QIcon, QFontMetrics, QCursor, QDesktopServices
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QGraphicsDropShadowEffect,
    QHeaderView, QTableWidgetItem, QAbstractItemView, QLabel, QListWidgetItem
)
import ApGuide.FunctionApGuide as ApGuide
from CalGrowth import *
from Posts.FunctionPosts import Posts


import time

img_back_path = 'Gui/Useimages/background.png'
icon_path = 'Gui/Useimages/icon.png'
window_title = '블루 스케줄러'
mainscreen_path = 'Gui\Screen.ui'
container_cal_path = 'Gui\Container.ui'
container_char_path = 'Gui\Container_char.ui'
list_char = []
list_oparts = ["네브라", "파에스토스","볼프세크","님루드","만드라고라","로혼치","에테르","안티키테라","보이니치","하니와",
            "토템폴","전지","콜간테","위니페소키","인형","아틀란티스"]
list_academy = ["백귀야행", "붉은겨울","트리니티","게헨나","아비도스","밀레니엄","아리우스","산해경","발키리"]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        loadUi(mainscreen_path,self)
        pixmap = QPixmap(img_back_path)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)

        icon = QIcon(icon_path)
        self.setWindowIcon(icon)
        self.setWindowTitle(window_title)

        # 메뉴바
        self.button_screen_menu1.clicked.connect(self.show_screen1)
        self.button_screen_menu2.clicked.connect(self.show_screen2)
        self.button_screen_menu3.clicked.connect(self.show_screen3)
        self.button_screen_menu4.clicked.connect(self.show_screen4)
        
        # # Home - 슬라이드쇼
        # posts = Posts()
        # self.url_slideshow = posts.getUpdateUrl()
        # asyncio.run(posts.getImages(self.url_slideshow))
        # self.label_slide_home.setScaledContents(True)
        # self.label_slide_home.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0))
        # if os.path.isdir('Posts/Images'):
        #     files = os.listdir('Posts/Images')
        #     files_path = ['Posts/Images/' + file for file in files]
        #     self.images = files_path
        #     self.current_image = 0
        #     self.setImage()
        #     self.timer = QTimer()
        #     self.timer.timeout.connect(self.next_image)
        #     self.timer.start(3000)
        # self.pushButton_slide_home.clicked.connect(self.clicked_image)

        # # Home - 공지사항, 주요소식
        # list_mainTopic, list_notice = posts.getNotice()
        # self.createTable(self.tableWidget_home1, list_notice)
        # self.createTable(self.tableWidget_home2, list_mainTopic)

        # @atexit.register
        # def close_driver():
        #     posts.driver.quit()
        #     if os.path.isfile(pid_file):
        #         os.remove(pid_file)
        #     FunctionCalGrowth.closeDB(self.j_database)

        # 재화계산
        self.j_database, self.json_datas, self.json_table_exp, self.json_table_credit, self.json_table_skill = FunctionCalGrowth.openDB()
        self.db_list_char = FunctionCalGrowth.readCharList(self.json_datas)
        
        self.calgrowth_layout(list_char, 'character', container_char_path, self.listWidget_cal1)
        self.calgrowth_layout(list_oparts, 'oparts', container_cal_path, self.listWidget_cal2)
        self.calgrowth_layout(list_academy, 'academy', container_cal_path, self.listWidget_cal3)
        self.calgrowth_layout(list_academy, 'academy', container_cal_path, self.listWidget_cal4)
        
        self.button_calgrowth_insert.clicked.connect(self.calgrowth_insert)
        self.button_calgrowth_delete.clicked.connect(self.calgrowth_delete)
        # item = self.listWidget_cal1.item(2)
        # label_img = item.data(Qt.ItemDataRole.DisplayRole)
        # print(label_img.text())

        # AP 가이드
        self.dateEdit_ap1.setDate(QDate.currentDate())
        self.button_ap1.clicked.connect(self.ap_image_save)
        self.button_ap2.clicked.connect(self.ap_image_link)

    # 메뉴바
    def show_screen1(self):
        self.stackedWidget.setCurrentIndex(0)
    def show_screen2(self):
        self.stackedWidget.setCurrentIndex(1)
    def show_screen3(self):
        self.stackedWidget.setCurrentIndex(2)
    def show_screen4(self):
        self.stackedWidget.setCurrentIndex(3)

    # Home - 슬라이드쇼
    def setImage(self):
        pixmap = QPixmap(self.images[self.current_image])
        self.label_slide_home.setPixmap(pixmap)
    def next_image(self):
        self.current_image = (self.current_image + 1) % len(self.images)
        self.setImage()
    def clicked_image(self):
        webbrowser.open_new_tab(self.url_slideshow)
 
    # Home - 공지글 layout
    def createTable(self, tableWidget, list):
        tableWidget.setRowCount(len(list))
        tableWidget.setShowGrid(False)
        tableWidget.horizontalHeader().setVisible(False)
        tableWidget.verticalHeader().setVisible(False)
        tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        tableWidget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        tableWidget.setStyleSheet("""
            QTableWidget {background-color: rgba(0,0,0,80);}
            #label_notice:hover {
                color: rgba(131,96,53,255);
            }   
        """)
                
        header = tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(1,50)

        for idx, post in enumerate(list):
            # title 추가
            label = ClickableLabel('',post['link'])
            font_metrics = QFontMetrics(label.font())
            elided_text = font_metrics.elidedText(post['title'], Qt.TextElideMode.ElideRight, label.width()-250)
            label.setText(elided_text)
            label.setObjectName('label_notice')
            label.setToolTip(post['title'])
            label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            if post['new']==1:
                label.setStyleSheet("color: red ; font-weight: bold;")

            tableWidget.setCellWidget(idx,0,label)
            # date 추가
            date_item = QTableWidgetItem(post['date'])
            tableWidget.setItem(idx, 1, date_item)

    # 재화계산 - layout
    def calgrowth_layout(self, list_item, item_type, container_path, listwidget):
        if listwidget is self.listWidget_cal1:
                listwidget.setDragEnabled(True)
                listwidget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
                listwidget.setDropIndicatorShown(True)
                listwidget.viewport().installEventFilter(self)

        for i in range(len(list_item)):
            container_ui = loadUi(container_path)
            container = QListWidgetItem(listwidget)
            container.setSizeHint(QSize(0,50))
            container_ui.label_img.setScaledContents(True)
            container_ui.label_img.setContentsMargins(3,3,3,3)
            for row in range(container_ui.tableWidget_cal.rowCount()):
                for column in range(container_ui.tableWidget_cal.columnCount()):
                     item_value = row+column
                     item = QTableWidgetItem(str(item_value))
                     item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                     container_ui.tableWidget_cal.setItem(row, column, item)

            if listwidget is self.listWidget_cal1:
                container_ui.comboBox.addItems(self.db_list_char)
                container_ui.comboBox.currentTextChanged.connect(self.on_combo_box_changed)
                char_name = container_ui.comboBox.currentText()
                img_path = f"Gui/Useimages/{item_type}/{char_name}.webp"
                # 여기다가 오파츠, 아카데미
            else:
                img_path = f"Gui/Useimages/{item_type}/{i+1:02}.webp"
            pixmap = QPixmap(img_path)
            container_ui.label_img.setPixmap(pixmap)
            container_ui.label_name.setText(list_item[i])
            listwidget.addItem(container)
            listwidget.setItemWidget(container, container_ui)
    
    def calgrowth_insert(self):
        listwidget = self.listWidget_cal1
        container_path = 'Gui\Container_char.ui'
        container_ui = loadUi(container_path)
        container = QListWidgetItem(listwidget)
        container.setSizeHint(QSize(0,50))
        container_ui.label_img.setScaledContents(True)
        container_ui.label_img.setContentsMargins(3,3,3,3)
        # img_path = f"Gui/Useimages/'character'/{i+1:02}.webp"
        # pixmap = QPixmap(img_path)
        # container_ui.label_img.setPixmap(pixmap)
        for row in range(container_ui.tableWidget_cal.rowCount()):
            for column in range(container_ui.tableWidget_cal.columnCount()):
                    item = QTableWidgetItem('0')
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    container_ui.tableWidget_cal.setItem(row, column, item)
        
        container_ui.comboBox.addItems(self.db_list_char)
        container_ui.comboBox.setCurrentText("")
        container_ui.comboBox.currentTextChanged.connect(self.on_combo_box_changed)
        listwidget.addItem(container)
        listwidget.setItemWidget(container, container_ui)
    
    def calgrowth_delete(self):
        listwidget = self.listWidget_cal1
        index = self.listWidget_cal1.currentRow()
        if index >= 0:
            listwidget.takeItem(index)

    def on_combo_box_changed(self):
        widget = self.sender().parent()
        row = self.listWidget_cal1.indexAt(widget.pos()).row()
        print(f"콤보박스가 listWidget_cal1의 {row}번째 아이템에 속해 있습니다.")
        self.listWidget_cal1.setCurrentRow(row)
        container_ui = self.listWidget_cal1.itemWidget(self.listWidget_cal1.currentItem())
        char_name = container_ui.comboBox.currentText()
        img_path = f"Gui/Useimages/character/{char_name}.webp"            
        pixmap = QPixmap(img_path)
        widget.label_img.setPixmap(pixmap)
    
    def printChanged(self, row, column):
        item = self.item(row, column)
        print(f'Cell ({row}, {column}) 값이 변경됨: {item.text()}')

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.Drop:
            pos = event.position()
            index = self.listWidget_cal1.indexAt(QPoint(int(pos.x()), int(pos.y())))
            current_row = self.listWidget_cal1.currentRow()
            if current_row == self.listWidget_cal1.count()-1 and index.row()==-1:
                return True
        return super().eventFilter(source, event)

    # 버튼 기능 - AP 가이드
    def ap_image_save(self):
        event_str = self.textEdit_ap1.toPlainText()
        date_str = self.dateEdit_ap1.date().toString('yyyy/MM/dd')
        time_start_str = self.timeEdit_ap1.time().toString('hh:mm')
        time_end_str = self.timeEdit_ap2.time().toString('hh:mm')
        time_spare_str = self.spinBox_ap1.value()
        ApGuide.ImgSave(event_str, date_str, time_start_str, time_end_str, time_spare_str)

        filepath = 'Images/'+event_str+' AP 가이드.webp'
        if os.path.exists(filepath):
            self.label_ap5.setPixmap(QPixmap(filepath))
            self.label_ap5.setScaledContents(True) 
        else:
            print("NO FILE")
       
        self.change_label_color1()
        self.timer = QTimer()
        self.timer.start(1500)
        self.timer.timeout.connect(self.change_label_color2)
    
    def change_label_color1(self):
        self.label_ap6.setStyleSheet("background-color: rgba(0,0,0,210); color:rgba(255,255,255,210); border-radius:20px;")

    def change_label_color2(self):
        self.timer.stop()
        self.label_ap6.setStyleSheet("background-color: rgba(0,0,0,0); color:rgba(255,255,255,0); border-radius:20px;")

    def ap_image_link(self):
        if os.path.isdir('Images') == False:
            os.mkdir('Images')
        folder_path = os.path.dirname(__file__)
        explorer_command = "explorer.exe"
        subprocess.Popen([explorer_command, folder_path+'\Images'])

class ClickableLabel(QLabel):
    def __init__(self, text, link):
        super().__init__(text)
        self.link = link

    def mouseReleaseEvent(self, event):
        QDesktopServices.openUrl(QUrl(self.link))

if __name__ == '__main__':
    pid_file = 'my.pid'
    if os.path.isfile(pid_file):
        print('Already running')
    else:
        with open(pid_file, 'w') as f:
            f.write(str(os.getpid()))
        print('Start program')

    app = QApplication(sys.argv)
    ttime_2 = time.time()
    window = MainWindow()
    ttime_3 = time.time()
    window.show()
    print("----------------------------------")
    print('MainWIndow 시간' ,ttime_3 - ttime_2)
    sys.exit(app.exec())
