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

# - 이미지 출처 : 블루 아카이브 디지털 굿즈샵 (https://forum.nexon.com/bluearchive/board_view?thread=1881343)

import sys
import os
import subprocess
import webbrowser

from PyQt6.QtCore import QDate, QTimer, Qt
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QGraphicsDropShadowEffect, QHeaderView, QTableWidgetItem, QAbstractItemView
)
from PyQt6.uic import loadUi

import ApGuide.FunctionApGuide as ApGuide
from Posts.FunctionPosts import Posts


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        img_back_path = 'Gui/images/28.png'
        icon_path = 'Gui/images/1-9.png'
        window_title = '블루 스케줄러'

        loadUi('Gui\Screen.ui',self)
        
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


        # Home - 슬라이드쇼
        posts = Posts()
        self.url_slideshow = posts.getImages()
        self.label_slide_home.setScaledContents(True)
        self.label_slide_home.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0))
        if os.path.isdir('Posts/Images'):
            files = os.listdir('Posts/Images')
            files_path = ['Posts/Images/' + file for file in files]
            self.images = files_path
            self.current_image = 0
            self.setImage()
            self.timer = QTimer()
            self.timer.timeout.connect(self.next_image)
            self.timer.start(3000)
        self.pushButton_slide_home.clicked.connect(self.clicked_image)

        # Home - 공지사항, 주요소식
        list_mainTopic, list_notice = posts.getNotice()
        self.createTable(self.tableWidget_home1, list_notice)
        self.createTable(self.tableWidget_home2, list_mainTopic)

        # AP 가이드
        self.dateEdit_ap1.setDate(QDate.currentDate())
        self.button_ap1.clicked.connect(self.ap_image_save)
        self.button_ap2.clicked.connect(self.ap_image_link)


    # 버튼 기능 - 메뉴바
    def show_screen1(self):
        self.stackedWidget.setCurrentIndex(0)
    def show_screen2(self):
        self.stackedWidget.setCurrentIndex(1)
    def show_screen3(self):
        self.stackedWidget.setCurrentIndex(2)
    def show_screen4(self):
        self.stackedWidget.setCurrentIndex(3)

    # 슬라이드쇼 - Home
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
                
        header = tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(1,100)

        for idx, post in enumerate(list):
            # title 추가
            # <a style='color: black; text-decoration:none;'href="https://www.naver.com">[진행 이벤트] 그건 모르지</a>
            title_item = QTableWidgetItem(post['title'])
            title_item.setToolTip(post['title'])
            tableWidget.setItem(idx, 0, title_item)
            # date 추가
            date_item = QTableWidgetItem(post['date'])
            tableWidget.setItem(idx, 1, date_item)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
