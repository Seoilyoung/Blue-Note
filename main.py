# 추가 기능
# - 일정(이벤트, 총력전 등)
# 	이건 수동으로 해야 하는거 아닌가? 달력형식, 목록형식으로 구현.
# - 인게임 연동도 가능한가?(AP, 카페, 숙제, 순위 확인)
# - 함수들 각 py파일로 이동할 수 있으면 옮기자. main이 더럽다

# - 이미지 출처 : 블루 아카이브 디지털 굿즈샵 (https://forum.nexon.com/bluearchive/board_view?thread=1881343)
#                블루 아카이브 - 나무위키

import sys
import os
import subprocess
import webbrowser
import asyncio
import random
import time
import threading
import requests
import datetime

from PyQt6.QtCore import QDate, QTimer, Qt, QUrl, QSize, QPoint, QEvent, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QIcon, QFontMetrics, QCursor, QDesktopServices, QColor, QPainter, QFont, QFontDatabase
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QGraphicsDropShadowEffect,
    QHeaderView, QTableWidgetItem, QAbstractItemView, QLabel, QListWidgetItem, QItemDelegate,
    QWidget, QCompleter
)
from PIL import Image, ImageCms
from io import BytesIO

import ApGuide.FunctionApGuide as ApGuide
from CalGrowth import *
from Posts.FunctionPosts import Posts

img_back_path = 'Gui/Useimages/background.webp'
icon_path = 'Gui/Useimages/icon.ico'
window_title = '블루 스케줄러'
mainscreen_path = 'Gui\Screen.ui'
loadingscreen_path = 'Gui\Screen_Loading.ui'
container_cal_path = 'Gui\Container.ui'
container_char_path = 'Gui\Container_char.ui'
font_path = 'Gui\Font\BMJUA_ttf.ttf'

class CrawlThread(QThread):
    progressChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        self.crawl_complete = False  # 크롤링 완료 플래그
        # 프로그래스바
        progress_thread = threading.Thread(target=self.run_progress)
        progress_thread.start()

        # URL, 제목리스트 추출
        asyncio.run(self.home_crwaling())
       
        # 작업이 완료되면 프로그래스바 스레드 종료 및 finished 시그널 발생
        progress_thread.join()
        self.finished.emit()
    
    # 프로그래스바
    def run_progress(self):
        for i in range(51):
            self.progressChanged.emit(i)
            time.sleep(0.1)
            if self.crawl_complete:
                break

    # Home
    async def home_crwaling(self):
        posts = Posts()
        self.url_update, self.url_images = await posts.get_images()
        self.maintopics = await posts.get_maintopic()
        self.notices = await posts.get_notice()
        self.crawl_complete = True

class LoadingWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 스티커 지정
        sticker_folder_path = './Gui/Useimages/sticker/'
        if os.path.isdir(sticker_folder_path):
            count_sticker = len(os.listdir(sticker_folder_path))
        # 스티커 번호 랜덤
        num_sticker = random.randrange(1,count_sticker)
        loadUi(loadingscreen_path,self)
        pixmap = QPixmap(sticker_folder_path + str(num_sticker) + '.webp')
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)

        self.setWindowTitle(window_title)
        self.setFixedSize(180,230)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.set_font(font_path)

        self.loading_window = LoadingWindow()
        self.loading_window.show()

        self.crawl_thread = CrawlThread()
        self.crawl_thread.progressChanged.connect(self.updateProgressBar)
        self.crawl_thread.finished.connect(self.onCrawlFinished)
        self.crawl_thread.finished.connect(self.loading_window.close)
        self.crawl_thread.start()
        
        loadUi(mainscreen_path,self)
        pixmap = QPixmap(img_back_path)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)

        icon = QIcon(icon_path)
        self.setWindowIcon(icon)
        self.setWindowTitle(window_title)
        self.setFixedSize(1280,730)

        # 메뉴바
        self.button_screen_menu1.clicked.connect(self.show_screen1)
        self.button_screen_menu2.clicked.connect(self.show_screen2)
        self.button_screen_menu3.clicked.connect(self.show_screen3)
        self.button_screen_menu4.clicked.connect(self.show_screen4)
        
        # 슬라이드쇼
        self.pushButton_slide_home.clicked.connect(self.clicked_image)


        # 재화계산화면
        self.json_Userdatas, self.json_datas, self.json_table_exp, self.json_table_credit, self.json_table_skill = FunctionCalGrowth.openDB()
        self.db_list_char = FunctionCalGrowth.readCharList(self.json_datas)
        sorted_list = sorted(self.json_Userdatas["Default"]["Student"], key=lambda k:self.json_Userdatas["Default"]["Student"][k]['index'])
        self.list_oparts = list(self.json_Userdatas["Default"]["Oparts"].keys())
        self.list_academy = list(self.json_Userdatas["Default"]["BD"].keys())
        self.calgrowth_layout(sorted_list, 'Character', container_char_path, self.listWidget_cal1)
        # class 생성 및 값 입력
        self.data_default = DataUser.dataset('default')
        self.data_default.update(self.json_Userdatas)
        # 재화 layout 구성
        self.calgrowth_layout(self.list_oparts, 'Oparts', container_cal_path, self.listWidget_cal2)
        self.calgrowth_layout(self.list_academy, 'BD', container_cal_path, self.listWidget_cal3)
        self.calgrowth_layout(self.list_academy, 'Note', container_cal_path, self.listWidget_cal4)
        
        # 기타 재화 layout
        self.material_layout()


        # 캐릭터 추가/제거 버튼
        self.button_calgrowth_insert.clicked.connect(self.calgrowth_insert)
        self.button_calgrowth_delete.clicked.connect(self.calgrowth_delete)

        # AP 가이드
        self.dateEdit_ap1.setDate(QDate.currentDate())
        self.button_ap1.clicked.connect(self.ap_image_save)
        self.button_ap2.clicked.connect(self.ap_image_link)

    def updateProgressBar(self, value):
        self.loading_window.progressBar.setValue(value)
        
    def onCrawlFinished(self):
        # 크롤링 작업이 완료되면 호출되는 콜백 함수
        self.loading_window.progressBar.setValue(100)
        time.sleep(0.5)
        
        # Home - 슬라이드쇼 링크
        self.label_slide_home.setScaledContents(True)
        self.label_slide_home.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0))

        self.current_image = 0
        self.setImageFromUrl(self.current_image)

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_image)
        self.timer.start(3000)
            
        # Home - 공지사항, 주요소식
        self.createTable(self.tableWidget_home1, self.crawl_thread.notices)
        self.createTable(self.tableWidget_home2, self.crawl_thread.maintopics)

        self.show()

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
    # qt.gui.imageio: libpng warning: iCCP: known incorrect sRGB profile
    # 해당 경고 해결을 위해 sRGB profile 제거
    def has_srgb_profile(self,image):
        """Check if the image has an sRGB ICC profile."""
        return "icc_profile" in image.info and image.info["icc_profile"] is not None
    def remove_srgb_profile(self, image):
        """Remove the sRGB ICC profile from the image."""
        if self.has_srgb_profile(image):
            src_profile = ImageCms.createProfile("sRGB")
            dest_profile = ImageCms.createProfile("sRGB")
            transform = ImageCms.buildTransform(src_profile, dest_profile, "RGB", "RGB", renderingIntent=0)
            img_without_profile = ImageCms.applyTransform(image, transform)
            return img_without_profile
        else:
            return image
    def setImageFromUrl(self, index):
        response = requests.get(self.crawl_thread.url_images[index])
        # 이미지 데이터를 PIL Image 객체로 로드
        image = Image.open(BytesIO(response.content))
        
        # 이미지에 sRGB 프로필이 있는 경우 제거
        image_without_srgb = self.remove_srgb_profile(image)
        
        # QPixmap으로 이미지 로드
        pixmap = QPixmap()
        with BytesIO() as f:
            image_without_srgb.save(f, format='PNG')
            f.seek(0)
            pixmap.loadFromData(f.read())
            
        self.label_slide_home.setPixmap(pixmap)
    def next_image(self):
        self.current_image = (self.current_image + 1) % len(self.crawl_thread.url_images)
        self.setImageFromUrl(self.current_image)
    def clicked_image(self):
        webbrowser.open_new_tab(self.crawl_thread.url_update)
 
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
            QTableWidget {
                background-color: rgba(0,0,0,128);
                color : white;            
            }
            #label_notice:hover {
                color: rgba(131,96,53,255);
            }   
        """)
                
        header = tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(1,50)

        current_unix_time = int(time.time())
        day3_time = 259200

        for idx, post in enumerate(list):
            # title 추가
            link = f"https://forum.nexon.com/bluearchive/board_view?board={post['boardId']}&thread={post['threadId']}"
            label = ClickableLabel('',link)
            
            font_metrics = QFontMetrics(label.font())
            elided_text = font_metrics.elidedText(post['title'], Qt.TextElideMode.ElideRight, label.width()-250)
            label.setText(elided_text)
            label.setObjectName('label_notice')
            label.setToolTip(post['title'])
            label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            is_recent = (current_unix_time - post['createDate'] < day3_time)
            label.setProperty('isRecent', is_recent)

            tableWidget.setCellWidget(idx,0,label)
            # date 추가
            formated_date = (datetime.datetime.utcfromtimestamp(post['createDate']) + datetime.timedelta(hours=9)).strftime("%m/%d")
            date_item = QTableWidgetItem(formated_date)
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
            container_ui.label_img.setScaledContents(True)
            container_ui.label_img.setContentsMargins(3,3,3,3)
            
            # 캐릭터 리스트
            if listwidget is self.listWidget_cal1:
                # 높이 96
                container.setSizeHint(QSize(0,98))
                # 콤보박스 드롭다운 목록 추가
                container_ui.comboBox.wheelEvent = self.ignore_wheel_event
                container_ui.comboBox.addItems(self.db_list_char)
                # 콤보박스 Completer를 이용한 자동완성
                completer = QCompleter(container_ui.comboBox.model())
                container_ui.comboBox.setCompleter(completer)
                # 테이블 셀 가로 길이
                for columnIndex in range(0,4):
                    container_ui.tableWidget_cal.setColumnWidth(columnIndex, 24)

                # 테이블 숫자 범위 제한
                delegate = RangeDelegate()
                container_ui.tableWidget_cal.setItemDelegate(delegate)

                #캐릭터 이미지
                char_name = list_item[i]
                container_ui.comboBox.setCurrentText(char_name)
                img_path = f"Gui/Useimages/{item_type}/{char_name}.webp"
                
                #캐릭터 데이터 불러오기
                academy = FunctionCalGrowth.readCharAcademy(self.json_datas, char_name)
                oparts_main = FunctionCalGrowth.readCharMainOparts(self.json_datas, char_name)
                oparts_sub = FunctionCalGrowth.readCharSubOparts(self.json_datas, char_name)
                memo = FunctionCalGrowth.readCharMemo(self.json_Userdatas, char_name)
                #캐릭터 데이터 출력
                if academy is not None and oparts_main is not None and oparts_sub is not None:
                    container_ui.label_academy.setText(academy)
                    container_ui.label_oparts_main.setText(oparts_main)
                    container_ui.label_oparts_sub.setText(oparts_sub)
                    container_ui.plainTextEdit.setPlainText(memo)
                # 테이블위젯 value 설정
                for j in range(4):
                    item_goal = QTableWidgetItem(str(self.json_Userdatas["Default"]["Student"][char_name]["skill_goal"][j]))
                    item_goal.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    container_ui.tableWidget_cal.setItem(0, j, item_goal)
                    item = QTableWidgetItem(str(self.json_Userdatas["Default"]["Student"][char_name]["skill_current"][j]))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    container_ui.tableWidget_cal.setItem(1, j, item)
                    
                    # 해방 테이블
                    if j>=1:
                        item_goal = QTableWidgetItem(str(self.json_Userdatas["Default"]["Student"][char_name]["liberation_goal"][j-1]))
                        item_goal.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        container_ui.tableWidget_cal.setItem(2, j, item_goal)
                        item = QTableWidgetItem(str(self.json_Userdatas["Default"]["Student"][char_name]["liberation_current"][j-1]))
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        container_ui.tableWidget_cal.setItem(3, j, item)
                
                # 테이블위젯 안쓰는 셀 비활성화
                for row in [2,3]:
                    if row < container_ui.tableWidget_cal.rowCount():  # Check if the row index is within the range
                        item = QTableWidgetItem()
                        item.setBackground(QColor('lightgray'))
                        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)  # Disable the item
                        container_ui.tableWidget_cal.setItem(row, 0, item)  # Adjust row index to 0-based

                # 아이템 이벤트 추가
                # 마지막에 추가하는 이유는 처음 초기값에서 JSON의 값을 넣을 때 마다 이벤트가 발생하고 그로 인해 버그가 발생하는데 이를 예방하기 위함
                container_ui.comboBox.currentTextChanged.connect(self.on_combo_box_changed)
                container_ui.tableWidget_cal.cellChanged.connect(self.on_table_cell_changed)
                container_ui.plainTextEdit.textChanged.connect(self.on_text_changed)
                # 캐릭터별 필요 재화 계산
                FunctionCalGrowth.calSkillTable(self.json_Userdatas, self.json_table_skill, self.json_datas, char_name)

            # 오파츠/BD/노트 리스트
            else:
                #높이 50
                container.setSizeHint(QSize(0,50))
                # 이미지
                if item_type == 'BD' or item_type == 'Note':
                    img_path = f"Gui/Useimages/Academy/{i+1:02}.webp"
                else:
                    img_path = f"Gui/Useimages/{item_type}/{i+1:02}.webp"
                # 테이블위젯. 
                list_insert = self.data_default.printItem(item_type,list_item[i])
                for j in range(4):
                    item_goal = QTableWidgetItem(str(list_insert[3-j]))
                    item_goal.setFlags(Qt.ItemFlag.ItemIsSelectable)
                    item_goal.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    container_ui.tableWidget_cal.setItem(0, j, item_goal)
                    item = QTableWidgetItem(str(self.json_Userdatas["Default"][item_type][list_item[i]][3-j]))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    container_ui.tableWidget_cal.setItem(1, j, item)
                    
                    if int(item_goal.text()) <= int(item.text()):
                        item.setBackground(QColor(0, 0, 0, 80))
                        item.setForeground(QColor(255, 255, 255))
                        item_goal.setBackground(QColor(0, 0, 0,80))
                        item_goal.setForeground(QColor(255, 255, 255))
                    else:
                        item.setBackground(QColor(255, 255, 255))
                        item.setForeground(QColor(0, 0, 0))
                        item_goal.setBackground(QColor(255, 255, 255))
                        item_goal.setForeground(QColor(0, 0, 0, 150))
                container_ui.tableWidget_cal.cellChanged.connect(lambda row, column: self.on_table_cell_changed2(row, column) if row == 1 else None)
 
            if os.path.isfile(img_path):
                pixmap = QPixmap(img_path)
                container_ui.label_img.setPixmap(pixmap)
                container_ui.label_name.setText(list_item[i])
            else:
                container_ui.label_img.setText("Default")
                container_ui.label_name.clear()

            listwidget.addItem(container)
            listwidget.setItemWidget(container, container_ui)

    # 재료 layout
    def material_layout(self):
        # layout 구성
        def set_label_content(label_img, label_name, img_path, text):
            pixmap = QPixmap(img_path)
            label_img.setPixmap(pixmap)
            label_name.setText(text)
        
        # 이미지 경로, 출력할 텍스트
        img_paths = [
        ("Gui/Useimages/WB/0_체육 WB.webp", "체육 WB"),
        ("Gui/Useimages/WB/1_사격 WB.webp", "사격 WB"),
        ("Gui/Useimages/WB/2_위생 WB.webp", "위생 WB"),
        ("Gui/Useimages/Etc/비의서.webp", "비의서"),
        ("Gui/Useimages/Etc/크레딧.webp", "크레딧")
        ]

        # 연결할 label
        labels = [
            (self.label_img_wb_1, self.label_name_wb_1),
            (self.label_img_wb_2, self.label_name_wb_2),
            (self.label_img_wb_3, self.label_name_wb_3),
            (self.label_img_secretnote, self.label_name_secretnote),
            (self.label_img_credit, self.label_name_credit)
        ]

        for (img_path, text), (label_img, label_name) in zip(img_paths, labels):
            set_label_content(label_img, label_name, img_path, text)

        #목표 재화 변수 불러오기 
        Report = self.data_default.Report
        Credit = self.data_default.Credit
        Secretnote = self.data_default.Secretnote
        wb = self.data_default.wb

        # 현재 보고서관련 gui, 기능 없음. 추후 추가 예정
        # layout 재화 입력
        self.update_material_layout(Credit, self.json_Userdatas["Default"]["Credit"], self.tableWidget_credit)
        self.update_material_layout(Secretnote, self.json_Userdatas["Default"]["Secretnote"], self.tableWidget_secretnote)
        self.update_material_layout(wb[0], self.json_Userdatas["Default"]["wb"][0], self.tableWidget_wb_1)
        self.update_material_layout(wb[1], self.json_Userdatas["Default"]["wb"][1], self.tableWidget_wb_2)
        self.update_material_layout(wb[2], self.json_Userdatas["Default"]["wb"][2], self.tableWidget_wb_3)   
    # 재료 layout 업데이트
    def update_material_layout(self, data_goal, data_current, tablewidget):
        material_goal = QTableWidgetItem(str(data_goal))
        material_goal.setFlags(Qt.ItemFlag.ItemIsSelectable)
        material_goal.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        tablewidget.setItem(0,0,material_goal)
        material_current = QTableWidgetItem(str(data_current))
        material_current.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        tablewidget.setItem(1,0,material_current)
        tablewidget.cellChanged.connect(lambda row, column: self.on_table_cell_changed3() if row == 1 else None)


    # 버튼 - 캐릭터 추가
    def calgrowth_insert(self):
        listwidget = self.listWidget_cal1
        container_path = 'Gui\Container_char.ui'
        container_ui = loadUi(container_path)
        container = QListWidgetItem(listwidget)
        container.setSizeHint(QSize(0,98))
        container_ui.comboBox.wheelEvent = self.ignore_wheel_event
        container_ui.label_img.setScaledContents(True)
        container_ui.label_img.setContentsMargins(3,3,3,3)
        
        container_ui.comboBox.addItems(self.db_list_char)
        container_ui.comboBox.setCurrentText("")
        delegate = RangeDelegate()
        container_ui.tableWidget_cal.setItemDelegate(delegate)
        container_ui.comboBox.currentTextChanged.connect(self.on_combo_box_changed)
        container_ui.tableWidget_cal.cellChanged.connect(self.on_table_cell_changed)
        listwidget.addItem(container)
        listwidget.setItemWidget(container, container_ui)
        FunctionCalGrowth.insertStudent(self.json_Userdatas, listwidget.count()-1, "Default "+str(listwidget.count()-1), "", "", "")
        self.json_Userdatas = FunctionCalGrowth.openDBuser()
    # 버튼 - 캐릭터 제거
    def calgrowth_delete(self):
        listwidget = self.listWidget_cal1
        index = self.listWidget_cal1.currentRow()
        if index >= 0:
            FunctionCalGrowth.deleteStudent(self.json_Userdatas, index)
            self.json_Userdatas = FunctionCalGrowth.openDBuser()
            # class 반영
            self.update_class()
            listwidget.takeItem(index)
    # 콤보박스 값 변경 이벤트 처리
    def on_combo_box_changed(self, char_name):
        
        widget = self.sender().parent()
        row = self.listWidget_cal1.indexAt(widget.pos()).row()
        # print(f"on_combo_box_changed 콤보박스가 listWidget_cal1의 {row}번째 아이템에 속해 있습니다.")
        self.listWidget_cal1.setCurrentRow(row)
        container_ui = self.listWidget_cal1.itemWidget(self.listWidget_cal1.currentItem())
        if container_ui is not None:
            img_path = f"Gui/Useimages/character/{char_name}.webp"
            pixmap = QPixmap(img_path)
            if os.path.isfile(img_path):
                widget.label_img.setPixmap(pixmap)
                academy = FunctionCalGrowth.readCharAcademy(self.json_datas, char_name)
                oparts_main = FunctionCalGrowth.readCharMainOparts(self.json_datas, char_name)
                oparts_sub = FunctionCalGrowth.readCharSubOparts(self.json_datas, char_name)
                container_ui.label_academy.setText(academy)
                container_ui.label_oparts_main.setText(oparts_main)
                container_ui.label_oparts_sub.setText(oparts_sub)
                # json 연동
                if char_name in self.json_Userdatas['Default']['Student'] and self.json_Userdatas['Default']['Student'][char_name]['index'] != row:
                    # if char_name != widget.label_name.text():
                    widget.label_img.clear()
                    widget.label_img.setText("중복 학생")
                    widget.label_name.setText("")
                    FunctionCalGrowth.initStudent(self.json_Userdatas, row, "Default "+str(row))
                    self.json_Userdatas = FunctionCalGrowth.openDBuser()
                else:
                    FunctionCalGrowth.updateStudent(self.json_Userdatas, row, char_name, academy, oparts_main, oparts_sub)
                    self.json_Userdatas = FunctionCalGrowth.openDBuser()
                    widget.label_name.setText(char_name)
                FunctionCalGrowth.calSkillTable(self.json_Userdatas, self.json_table_skill, self.json_datas, char_name)
            else:
                container_ui.label_img.setText("Default")
                container_ui.label_name.clear()
                container_ui.label_academy.setText("")
                container_ui.label_oparts_main.setText("")
                container_ui.label_oparts_sub.setText("")
                FunctionCalGrowth.initStudent(self.json_Userdatas, row, char_name)
                self.json_Userdatas = FunctionCalGrowth.openDBuser()
            # class 반영
            self.update_class()
    # 테이블 셀 값 변경 이벤트 처리
    def on_table_cell_changed(self,cell_row,cell_column):
        widget = self.sender().parent()
        row = self.listWidget_cal1.indexAt(widget.pos()).row()
        # print(f"on_table_cell_changed 콤보박스가 listWidget_cal1의 {row}번째 아이템에 속해 있습니다.")
        self.listWidget_cal1.setCurrentRow(row)
        container_ui = self.listWidget_cal1.itemWidget(self.listWidget_cal1.currentItem())
        if container_ui is not None:
            char_name = container_ui.comboBox.currentText()
            item = container_ui.tableWidget_cal.item(cell_row, cell_column)
            
            self.json_Userdatas, result = FunctionCalGrowth.updateTable(self.json_Userdatas, row, cell_row, cell_column, int(item.text()))

            if result == 0:
                FunctionCalGrowth.calSkillTable(self.json_Userdatas, self.json_table_skill, self.json_datas, char_name)
                # class 반영
                self.update_class()
    # 텍스트박스 텍스트 변경 이벤트 처리
    def on_text_changed(self):
        # 해당 캐릭터의 row 확인
        widget = self.sender().parent()
        row = self.listWidget_cal1.indexAt(widget.pos()).row()
        # 작업할 row 설정
        self.listWidget_cal1.setCurrentRow(row)
        container_ui = self.listWidget_cal1.itemWidget(self.listWidget_cal1.currentItem())
        if container_ui is not None:
            char_name = container_ui.comboBox.currentText()
            memo = container_ui.plainTextEdit.toPlainText()

            FunctionCalGrowth.updateMemo(self.json_Userdatas, row, char_name, memo)
    
    # class 생성 및 값 입력 / 테이블 반영
    def update_class(self):
        # print("Update 클래스")
        self.data_default = DataUser.dataset('default')
        self.data_default.update(self.json_Userdatas)
        self.update_table_list(self.list_oparts, 'Oparts', self.listWidget_cal2)
        self.update_table_list(self.list_academy, 'BD', self.listWidget_cal3)
        self.update_table_list(self.list_academy, 'Note', self.listWidget_cal4)
        self.update_table('wb', self.tableWidget_wb_1)
        self.update_table('wb', self.tableWidget_wb_2)
        self.update_table('wb', self.tableWidget_wb_3)
        self.update_table('Credit', self.tableWidget_credit)
        self.update_table('Secretnote', self.tableWidget_secretnote)

    # 테이블 배경색 설정
    def set_cell_colors(self, item_goal, item_current):
        if int(item_goal.text()) <= int(item_current.text()):
            item_current.setBackground(QColor(0, 0, 0, 80))
            item_current.setForeground(QColor(255, 255, 255))
            item_goal.setBackground(QColor(0, 0, 0,80))
            item_goal.setForeground(QColor(255, 255, 255))
        else:
            item_current.setBackground(QColor(255, 255, 255))
            item_current.setForeground(QColor(0, 0, 0))
            item_goal.setBackground(QColor(255, 255, 255))
            item_goal.setForeground(QColor(0, 0, 0, 150))

    # 테이블 리스트 수정(2행 4열 테이블)
    def update_table_list(self, list_item, item_type, listWidget):
        for i in range(len(list_item)):
            container_ui = listWidget.itemWidget(listWidget.item(i))
            # 오파츠/BD/노트 리스트
            # 입력할 list
            item_insert = self.data_default.printItem(item_type,list_item[i])
            for j in range(4):
                item = QTableWidgetItem(str(item_insert[3-j]))
                item.setFlags(Qt.ItemFlag.ItemIsSelectable)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                container_ui.tableWidget_cal.setItem(0, j, item)
                item_goal = container_ui.tableWidget_cal.item(0, j)
                item_current = container_ui.tableWidget_cal.item(1, j)

                self.set_cell_colors(item_goal, item_current)

    # 테이블 수정(2행 1열 테이블)
    def update_table(self, item_type, TableWidget):
        item_insert = self.data_default.printItem(item_type)

        # 보고서 추가시 더 추가해야됨. 그건 얘들과 wb랑 성격이 달라서 위 list로 해야할지도?
        # wb는 list로 되어 있으니깐.
        if item_type == 'wb':
            if TableWidget == self.tableWidget_wb_1:
                item = QTableWidgetItem(str(item_insert[0]))
            elif TableWidget == self.tableWidget_wb_2:
                item = QTableWidgetItem(str(item_insert[1]))
            elif TableWidget == self.tableWidget_wb_3:
                item = QTableWidgetItem(str(item_insert[2]))
        else:
            # int값
            item = QTableWidgetItem(str(item_insert))

        item.setFlags(Qt.ItemFlag.ItemIsSelectable)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        TableWidget.setItem(0, 0, item)
        item_goal = TableWidget.item(0, 0)
        item_current = TableWidget.item(1, 0)

        self.set_cell_colors(item_goal, item_current)

    # listwidget 순서 변경 이벤트
    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.Drop:
            pos = event.position()
            index = self.listWidget_cal1.indexAt(QPoint(int(pos.x()), int(pos.y())))
            current_row = self.listWidget_cal1.currentRow()
            
            if (current_row == self.listWidget_cal1.count()-1 and index.row()==-1) or (index.row() == current_row+1 and pos.y()%50<25):
                return True
            FunctionCalGrowth.updateIndex(self.json_Userdatas, current_row, index.row())
        return super().eventFilter(source, event)
    # 오파츠, BD, 노트 테이블 변경 이벤트
    def on_table_cell_changed2(self,cell_row,cell_column):
        widget = self.sender().parent()
        if widget.parent() is not None:
            listWidget = widget.parent().parent()
            if listWidget == self.listWidget_cal2:
                item_type = "Oparts"
            if listWidget == self.listWidget_cal3:
                item_type = "BD"
            if listWidget == self.listWidget_cal4:
                item_type = "Note"
            row = listWidget.indexAt(widget.pos()).row()
            listWidget.setCurrentRow(row)
            container_ui = listWidget.itemWidget(listWidget.currentItem())
            if container_ui is not None:
                item_name = container_ui.label_name.text()
                item = container_ui.tableWidget_cal.item(cell_row, cell_column)
                item_goal = container_ui.tableWidget_cal.item(0, cell_column)
                
                self.set_cell_colors(item_goal,item)
                FunctionCalGrowth.updateTable2(self.json_Userdatas, item_type, item_name, cell_column, int(item.text()))
                self.json_Userdatas = FunctionCalGrowth.openDBuser()

    # 기타 재화 테이블 변경 이벤트
    def on_table_cell_changed3(self):
            table = self.sender()

            if table == self.tableWidget_wb_1:
                item_type = 'wb'
                cell_column = 0
            elif table == self.tableWidget_wb_2:
                item_type = 'wb'
                cell_column = 1
            elif table == self.tableWidget_wb_3:
                item_type = 'wb'
                cell_column = 2
            elif table == self.tableWidget_credit:
                item_type = 'Credit'
                cell_column = 0
            elif table == self.tableWidget_secretnote:
                item_type = 'Secretnote'
                cell_column = 0

            item = table.item(1, 0)
            item_goal = table.item(0, 0)
            self.set_cell_colors(item_goal,item)
            FunctionCalGrowth.updateTable2(self.json_Userdatas, item_type,'', cell_column, int(item.text()))
            self.json_Userdatas = FunctionCalGrowth.openDBuser()

    # 버튼 기능 - AP 가이드 저장
    def ap_image_save(self):
        print("저장")
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
        # else:
        #     print("NO FILE")
       
        self.change_label_color1()
        self.timer = QTimer()
        self.timer.start(1500)
        self.timer.timeout.connect(self.change_label_color2)
    
    def change_label_color1(self):
        self.label_ap6.setStyleSheet("background-color: rgba(0,0,0,210); color:rgba(255,255,255,210); border-radius:20px;")

    def change_label_color2(self):
        self.timer.stop()
        self.label_ap6.setStyleSheet("background-color: rgba(0,0,0,0); color:rgba(255,255,255,0); border-radius:20px;")

    # 버튼 기능 - AP 가이드 경로
    def ap_image_link(self):
        print("링크")
        if not os.path.isdir('Images'):
            os.mkdir('Images')


        # 스크립트가 실행 중인 디렉토리를 가져오기
        script_dir = os.path.dirname(sys.argv[0])

        # Images 디렉토리 경로 만들기
        image_dir = os.path.join(script_dir, 'Images')

        # 슬래시로 경로를 변경
        image_dir = image_dir.replace("/", "\\")

        explorer_command = "explorer.exe"
        subprocess.Popen([explorer_command, image_dir])
        
    #콤보박스 휠 이벤트 무시
    def ignore_wheel_event(self, event):
        event.ignore()

    # GUI 폰트 추가
    def set_font(self, fontpath):
        font_id = QFontDatabase.addApplicationFont(fontpath)

        if font_id == -1:
            print("폰트 로드 실패")
            return


# 공지사항 제목 라벨 속성 부여
class ClickableLabel(QLabel):
    def __init__(self, text, link):
        super().__init__(text)
        self.link = link
        self.isRecent = False
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet("""
            QLabel[isRecent="true"] {
                font-weight: bold;  /* 최근 게시물일 때 폰트 굵기는 볼드 */
            }
        """)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Define text colors
        outline_color = QColor(0, 0, 0)  # Black
        if self.property('isRecent'):
            text_color = QColor(231, 76, 60)  # Red for recent posts
        else:
            text_color = QColor(255, 255, 255)  # White

        # Draw outline
        font_metrics = QFontMetrics(self.font())
        text = self.text()
        elided_text = font_metrics.elidedText(text, Qt.TextElideMode.ElideRight, self.width())
        
        painter.setFont(self.font())
        if self.property('isRecent'):
            painter.setPen(outline_color)
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                painter.drawText(self.rect().adjusted(dx, dy, dx, dy), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, elided_text)

        # Draw text
        painter.setPen(text_color)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, elided_text)

    def mouseReleaseEvent(self, event):
        QDesktopServices.openUrl(QUrl(self.link))

class RangeDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setModelData(self, editor, model, index):
        try:
            value = int(editor.text())
            if index.row()==0 or index.row()==1:
                if index.column() == 0:
                    range_min, range_max = 1, 5
                else:
                    range_min, range_max = 1, 10
            elif index.row()==2 or index.row()==3:
                range_min, range_max = 0, 25
            value = min(max(range_min, value), range_max)
            model.setData(index, value, Qt.ItemDataRole.EditRole)
        except ValueError:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
