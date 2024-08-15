# 크롤링

import asyncio
import threading
import time

import os
from PyQt6.QtGui import QPixmap

from PyQt6.QtCore import QThread, pyqtSignal
from src.Posts.FunctionPosts import Posts as Posts
import src.config as config

class CrawlThread(QThread):
    progressChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_cache = ImageCache(config.useimage_path)

    def run(self):
        # 플래그 초기화 (크롤링, 캐싱)
        self.crawl_complete = False
        self.cache_complete = False

        # 프로그래스바
        # progress_thread = threading.Thread(target=self.run_progress)
        # progress_thread.start()
        self.progressChanged.emit(0)

        # URL, 제목리스트 추출
        print("Home Crawling 시작")
        asyncio.run(self.home_crwaling())
        self.progressChanged.emit(50)
        print("Home Crawling 완료")
        
        # 이미지 캐싱
        print("Image Caching 시작")
        asyncio.run(self.image_caching())
        self.progressChanged.emit(100)
        print("Image Caching 완료")

       
        # 작업이 완료되면 프로그래스바 스레드 종료 및 finished 시그널 발생
        # progress_thread.join()

        if not self.crawl_complete and not self.cache_complete:
            self.finished.emit()
            self.crawl_complete = True
            self.cache_complete = True
    
    # 프로그래스바
    def run_progress(self):
        for i in range(101):
            print(f"Progress: {i}%")
            self.progressChanged.emit(i)
            time.sleep(0.1)
            if self.crawl_complete and self.cache_complete:
                self.progressChanged.emit(100)
                break

    # Home
    async def home_crwaling(self):
        posts = Posts()
        self.url_update, self.url_images = await posts.get_images()
        self.progressChanged.emit(15)
        self.maintopics = await posts.get_maintopic()
        self.progressChanged.emit(30)
        self.notices = await posts.get_notice()
        self.progressChanged.emit(45)
        
        # self.crawl_complete = True
    
    async def image_caching(self):
        self.image_cache.load_all_image()

        self.cache_complete = True

class ImageCache:
    def __init__(self, base_path):
        self.base_path = base_path
        self.cache = {}
    
    def load_all_image(self):
        folders = ['Academy', 'Character', 'Etc', 'Oparts', 'WB']
        for folder in folders:
            folder_path = os.path.join(self.base_path, folder)
            for file_name in os.listdir(folder_path):
                image_path = os.path.join(folder_path, file_name)
                if os.path.isfile(image_path):
                    pixmap = QPixmap(image_path)
                    self.cache[os.path.join(folder, file_name)] = pixmap
    
    def get_image(self, relative_path):
        image = self.cache.get(relative_path, None)
        if image is None:
            print(relative_path + "불러오기 실패")
        return self.cache.get(relative_path, None)
    
    def get_imagelist(self):
        for image_path in self.cache.keys():
            print(image_path)