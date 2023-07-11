# 추가 기능
# - 일정(이벤트, 총력전 등)
# 	이건 수동으로 해야 하는거 아닌가? 달력형식, 목록형식으로 구현.
# - 인게임 연동도 가능한가?(AP, 카페, 숙제, 순위 확인)
# - 함수들 각 py파일로 이동할 수 있으면 옮기자. main이 더럽다

# - 이미지 출처 : 블루 아카이브 디지털 굿즈샵 (https://forum.nexon.com/bluearchive/board_view?thread=1881343)
#                블루아카이브 - 나무위키

import sys
import os
import subprocess
import webbrowser
import asyncio
import atexit

from PyQt6.QtCore import QDate, QTimer, Qt, QUrl, QSize, QPoint, QEvent, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QIcon, QFontMetrics, QCursor, QDesktopServices, QColor
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QGraphicsDropShadowEffect,
    QHeaderView, QTableWidgetItem, QAbstractItemView, QLabel, QListWidgetItem, QItemDelegate,
    QWidget
)
import ApGuide.FunctionApGuide as ApGuide
import threading
from CalGrowth import *
from Posts.FunctionPosts import Posts
import random
import time

img_back_path = 'Gui/Useimages/background.webp'
icon_path = 'Gui/Useimages/icon.webp'
window_title = '블루 스케줄러'
mainscreen_path = 'Gui\Screen.ui'
loadingscreen_path = 'Gui\Screen_Loading.ui'
container_cal_path = 'Gui\Container.ui'
container_char_path = 'Gui\Container_char.ui'

class CrawlThread(QThread):
    progressChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        self.crawl_complete = False  # 크롤링 완료 플래그
        # 프로그래스바
        progress_thread = threading.Thread(target=self.run_progress)
        progress_thread.start()

        # 크롤링
        asyncio.run(self.home_crwaling())

       
        # 작업이 완료되면 프로그래스바 스레드 종료 및 finished 시그널 발생
        progress_thread.join()
        self.finished.emit()
        self.posts.driver.quit()
    
    # 프로그래스바
    def run_progress(self):
        for i in range(101):
            self.progressChanged.emit(i)
            time.sleep(0.1)
            if self.crawl_complete:
                break

    # Home
    async def home_crwaling(self):
        
        self.posts = Posts()

        tasks = [
            self.posts.getUpdateUrl(),
            self.posts.getNotice()
        ]
        results = await asyncio.gather(*tasks)
        self.url_slideshow, (self.list_mainTopic, self.list_notice) = results

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

        icon = QIcon(icon_path)
        self.setWindowIcon(icon)
        self.setWindowTitle(window_title)
        self.setFixedSize(180,230)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

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
        
        # 재화계산
        self.json_Userdatas, self.json_datas, self.json_table_exp, self.json_table_credit, self.json_table_skill = FunctionCalGrowth.openDB()

        self.db_list_char = FunctionCalGrowth.readCharList(self.json_datas)
        sorted_list = sorted(self.json_Userdatas["Default"]["Student"], key=lambda k:self.json_Userdatas["Default"]["Student"][k]['index'])
        self.list_oparts = list(self.json_Userdatas["Default"]["Oparts"].keys())
        self.list_academy = list(self.json_Userdatas["Default"]["BD"].keys())
        self.calgrowth_layout(sorted_list, 'Character', container_char_path, self.listWidget_cal1)
        # class 생성 및 값 입력
        self.data_default = DataUser.dataset('default')
        self.data_default.update(self.json_Userdatas)

        self.calgrowth_layout(self.list_oparts, 'Oparts', container_cal_path, self.listWidget_cal2)
        self.calgrowth_layout(self.list_academy, 'BD', container_cal_path, self.listWidget_cal3)
        self.calgrowth_layout(self.list_academy, 'Note', container_cal_path, self.listWidget_cal4)
        
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
        
        # Home - 이미지쇼 링크
        self.label_slide_home.setScaledContents(True)
        self.label_slide_home.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0))

        if not os.path.exists('Posts'):
            os.makedirs('Posts')
        if not os.path.exists('Posts/Images'):
            os.makedirs('Posts/Images')

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
        self.createTable(self.tableWidget_home1, self.crawl_thread.list_notice)
        self.createTable(self.tableWidget_home2, self.crawl_thread.list_mainTopic)

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
    def setImage(self):
        pixmap = QPixmap(self.images[self.current_image])
        self.label_slide_home.setPixmap(pixmap)
    def next_image(self):
        self.current_image = (self.current_image + 1) % len(self.images)
        self.setImage()
    def clicked_image(self):
        # print(self.crawl_thread.url_slideshow)
        webbrowser.open_new_tab(self.crawl_thread.url_slideshow)
 
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
            QTableWidget {background-color: 
                            rgba(0,0,0,80);
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
                label.setStyleSheet("""QLabel {
                    color: red ;
                    font-weight: bold;
                } """)

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
            
            # 캐릭터 리스트
            if listwidget is self.listWidget_cal1:
                # 콤보박스 드롭다운 목록 추가
                container_ui.comboBox.wheelEvent = self.ignore_wheel_event
                container_ui.comboBox.addItems(self.db_list_char)
                # 테이블 숫자 범위 제한
                delegate = RangeDelegate()
                container_ui.tableWidget_cal.setItemDelegate(delegate)
                char_name = list_item[i]
                container_ui.comboBox.setCurrentText(char_name)
                if item_type == 'BD' or item_type == 'Note':
                    img_path = f"Gui/Useimages/Academy/{char_name}.webp"
                else:
                    img_path = f"Gui/Useimages/{item_type}/{char_name}.webp"
                academy = FunctionCalGrowth.readCharAcademy(self.json_datas, char_name)
                oparts_main = FunctionCalGrowth.readCharMainOparts(self.json_datas, char_name)
                oparts_sub = FunctionCalGrowth.readCharSubOparts(self.json_datas, char_name)
                if academy is not None and oparts_main is not None and oparts_sub is not None:
                    container_ui.label_academy.setText(academy)
                    container_ui.label_oparts_main.setText(oparts_main)
                    container_ui.label_oparts_sub.setText(oparts_sub)
                # 테이블위젯. 
                for j in range(4):
                    item_goal = QTableWidgetItem(str(self.json_Userdatas["Default"]["Student"][char_name]["skill_goal"][j]))
                    item_goal.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    container_ui.tableWidget_cal.setItem(0, j, item_goal)
                    item = QTableWidgetItem(str(self.json_Userdatas["Default"]["Student"][char_name]["skill_current"][j]))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    container_ui.tableWidget_cal.setItem(1, j, item)
                # 아이템 이벤트 추가
                # 마지막에 추가하는 이유는 처음 초기값에서 JSON의 값을 넣을 때 마다 이벤트가 발생하고 그로 인해 버그가 발생하는데 이를 예방하기 위함
                container_ui.comboBox.currentTextChanged.connect(self.on_combo_box_changed)
                container_ui.tableWidget_cal.cellChanged.connect(self.on_table_cell_changed)
                # 캐릭터별 필요 재화 계산
                self.json_Userdatas = FunctionCalGrowth.calSkillTable(self.json_Userdatas, self.json_table_skill, self.json_datas, char_name)

            # 오파츠/BD/노트 리스트
            else:
                # 이미지
                if item_type == 'BD' or item_type == 'Note':
                    img_path = f"Gui/Useimages/Academy/{i+1:02}.webp"
                else:
                    img_path = f"Gui/Useimages/{item_type}/{i+1:02}.webp"
                # 테이블위젯. 
                list_insert = self.data_default.printList(item_type,list_item[i])
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
 
            pixmap = QPixmap(img_path)
            container_ui.label_img.setPixmap(pixmap)
            container_ui.label_name.setText(list_item[i])
            listwidget.addItem(container)
            listwidget.setItemWidget(container, container_ui)
    
    # 버튼 - 캐릭터 추가
    def calgrowth_insert(self):
        listwidget = self.listWidget_cal1
        container_path = 'Gui\Container_char.ui'
        container_ui = loadUi(container_path)
        container = QListWidgetItem(listwidget)
        container.setSizeHint(QSize(0,50))
        container_ui.comboBox.wheelEvent = self.ignore_wheel_event
        container_ui.label_img.setScaledContents(True)
        container_ui.label_img.setContentsMargins(3,3,3,3)
        for row in range(container_ui.tableWidget_cal.rowCount()):
            for column in range(container_ui.tableWidget_cal.columnCount()):
                    item = QTableWidgetItem('0')
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    container_ui.tableWidget_cal.setItem(row, column, item)
        
        container_ui.comboBox.addItems(self.db_list_char)
        container_ui.comboBox.setCurrentText("")
        delegate = RangeDelegate()
        container_ui.tableWidget_cal.setItemDelegate(delegate)
        container_ui.comboBox.currentTextChanged.connect(self.on_combo_box_changed)
        container_ui.tableWidget_cal.cellChanged.connect(self.on_table_cell_changed)
        listwidget.addItem(container)
        listwidget.setItemWidget(container, container_ui)
        self.json_Userdatas = FunctionCalGrowth.insertStudent(self.json_Userdatas, listwidget.count()-1, "Default "+str(listwidget.count()-1), "", "", "")
    # 버튼 - 캐릭터 제거
    def calgrowth_delete(self):
        listwidget = self.listWidget_cal1
        index = self.listWidget_cal1.currentRow()
        container_ui = listwidget.itemWidget(self.listWidget_cal1.currentItem())
        char_name = container_ui.comboBox.currentText()
        if index >= 0:
            self.json_Userdatas = FunctionCalGrowth.deleteStudent(self.json_Userdatas, index)
            # class 반영
            self.update_class(container_ui.label_oparts_main.text(), container_ui.label_oparts_sub.text(), container_ui.label_academy.text())
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
            widget.label_img.setPixmap(pixmap)
            if os.path.isfile(img_path):
                academy = FunctionCalGrowth.readCharAcademy(self.json_datas, char_name)
                oparts_main = FunctionCalGrowth.readCharMainOparts(self.json_datas, char_name)
                oparts_sub = FunctionCalGrowth.readCharSubOparts(self.json_datas, char_name)
                container_ui.label_academy.setText(academy)
                container_ui.label_oparts_main.setText(oparts_main)
                container_ui.label_oparts_sub.setText(oparts_sub)
                # json 연동
                if char_name in self.json_Userdatas['Default']['Student']:
                    # if char_name != widget.label_name.text():
                    widget.label_img.clear()
                    widget.label_img.setText("중복 학생")
                    widget.label_name.setText("")
                    self.json_Userdatas = FunctionCalGrowth.initStudent(self.json_Userdatas, row, "Default "+str(row))
                else:
                    self.json_Userdatas = FunctionCalGrowth.updateStudent(self.json_Userdatas, row, char_name, academy, oparts_main, oparts_sub)
                    widget.label_name.setText(char_name)
                self.json_Userdatas = FunctionCalGrowth.calSkillTable(self.json_Userdatas, self.json_table_skill, self.json_datas, char_name)
            else:
                container_ui.label_academy.setText("")
                container_ui.label_oparts_main.setText("")
                container_ui.label_oparts_sub.setText("")
                self.json_Userdatas = FunctionCalGrowth.initStudent(self.json_Userdatas, row, char_name)
            # class 반영
            self.update_class(container_ui.label_oparts_main.text(), container_ui.label_oparts_sub.text(), container_ui.label_academy.text())
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
                self.json_Userdatas = FunctionCalGrowth.calSkillTable(self.json_Userdatas, self.json_table_skill, self.json_datas, char_name)
                # class 반영
                self.update_class(container_ui.label_oparts_main.text(), container_ui.label_oparts_sub.text(), container_ui.label_academy.text())
    # class 생성 및 값 입력 / 테이블 반영
    def update_class(self,oparts_main,oparts_sub,academy):
        # print("Update 클래스")
        self.data_default = DataUser.dataset('default')
        self.data_default.update(self.json_Userdatas)
        self.update_table(self.list_oparts, 'Oparts', self.listWidget_cal2)
        self.update_table(self.list_academy, 'BD', self.listWidget_cal3)
        self.update_table(self.list_academy, 'Note', self.listWidget_cal4)
    # 테이블 수정
    def update_table(self, list_item, item_type, listWidget):
        for i in range(len(list_item)):
            container_ui = listWidget.itemWidget(listWidget.item(i))
            # 오파츠/BD/노트 리스트
            list_insert = self.data_default.printList(item_type,list_item[i])
            for j in range(4):
                item = QTableWidgetItem(str(list_insert[3-j]))
                item.setFlags(Qt.ItemFlag.ItemIsSelectable)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                container_ui.tableWidget_cal.setItem(0, j, item)
                item_goal = container_ui.tableWidget_cal.item(0, j)
                item_current = container_ui.tableWidget_cal.item(1, j)

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
                    
    # listwidget 순서 변경 이벤트
    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.Drop:
            pos = event.position()
            index = self.listWidget_cal1.indexAt(QPoint(int(pos.x()), int(pos.y())))
            current_row = self.listWidget_cal1.currentRow()
            if (current_row == self.listWidget_cal1.count()-1 and index.row()==-1) or (index.row() == current_row+1 and pos.y()%50<25):
                return True
            self.json_Userdatas = FunctionCalGrowth.updateIndex(self.json_Userdatas, current_row, index.row())
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
                self.json_Userdatas = FunctionCalGrowth.updateTable2(self.json_Userdatas, item_type, item_name, cell_column, int(item.text()))
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

    def ap_image_link(self):
        if os.path.isdir('Images') == False:
            os.mkdir('Images')
        folder_path = os.path.dirname(__file__)
        explorer_command = "explorer.exe"
        subprocess.Popen([explorer_command, folder_path+'\Images'])
    #콤보박스 휠 이벤트 무시
    def ignore_wheel_event(self, event):
        event.ignore()

class ClickableLabel(QLabel):
    def __init__(self, text, link):
        super().__init__(text)
        self.link = link

    def mouseReleaseEvent(self, event):
        QDesktopServices.openUrl(QUrl(self.link))

class RangeDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setModelData(self, editor, model, index):
        try:
            value = int(editor.text())
            if index.column() == 0:
                range_min, range_max = 1, 5
            else:
                range_min, range_max = 1, 10
            value = min(max(range_min, value), range_max)
            model.setData(index, value, Qt.ItemDataRole.EditRole)
        except ValueError:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
