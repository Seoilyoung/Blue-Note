from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.request
import os
import glob

BASE_URL = 'https://forum.nexon.com/bluearchive/'

class Posts():
    def __init__(self):
        super().__init__()
        options = webdriver.EdgeOptions()
        options.add_argument("disable-logging")
        options.add_argument("headless")
        self.driver = webdriver.Edge(options=options, executable_path=EdgeChromiumDriverManager().install())

    def __del__(self):
        self.driver.quit()

    def download_image(self, url, filename):
        with urllib.request.urlopen(url) as response:
            with open(filename, 'wb') as file:
                file.write(response.read())

    def getImages(self):
        url_search = BASE_URL + '/board_list?keywords=%EC%83%81%EC%84%B8&board=1076&searchKeywordType=THREAD_TITLE'
        self.driver.get(url_search)
        soup_search = BeautifulSoup(self.driver.page_source, 'lxml')
        post_url = BASE_URL + soup_search.select('body div.list-box a')[0].get('href')

        self.driver.get(post_url)

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        posts = soup.select('body div.board-view div.section-bot div.view-box div.txt.note-editor p')

        if not os.path.isdir('./Posts/Images'):
            os.mkdir('./Posts/Images')
        
        for file in glob.glob("./Posts/Images/*.png"):
            os.remove(file)

        n=1
        for post in posts:
            img = post.find('img')
            if img and img.get('width') == '780' and img.get('height') == '438':    
                img_url = img.get('src')
                name, ext = os.path.splitext(img_url)
                filename = f"./Posts/Images/{n:02}.png"
                try:
                    self.download_image(img_url, filename)
                    n += 1
                except Exception as e:
                    print(f"Error download image {img_url}: {e}")

        return post_url

    def getMainTopic(self):
        self.driver.get(BASE_URL)

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        soup_extract = soup.body.extract()
        posts = soup_extract.select('body div.main.main-type2 div.section-bot div.sticky-box ul.swiper-slide.type-list.swiper-slide-active li')

        list_post = []
        for post in posts:
            if post.find('h3') is not None:
                # category = post.find('span',class_= 'key-color').text.strip()
                # icon = post.find('span',class_='icon-new')
                title = post.find('h3').text.strip()
                link = post.find('a').get('href')
                date_str = post.find('span', {'class':'date'})
                if date_str is not None:
                    date = datetime.strptime(date_str.text, '%Y.%m.%d').strftime('%m/%d')
                else:
                    date = ''
                list_post.append({"title":title, "link":link, "date":date})
                
        return list_post
    
    def getNotice(self):
        print("test")