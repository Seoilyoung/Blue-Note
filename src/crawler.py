# 크롤링

import asyncio
import threading
import time

from PyQt6.QtCore import QThread, pyqtSignal
from src.Posts.FunctionPosts import Posts as Posts

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