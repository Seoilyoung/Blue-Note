from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.request
import os, glob

base_url = 'https://forum.nexon.com/bluearchive/'

class Posts():
    def __init__(self):
        super().__init__()
        options = webdriver.EdgeOptions()
        options.add_argument("disable-logging")
        options.add_argument("headless")
        self.driver = webdriver.Edge(options=options, executable_path=EdgeChromiumDriverManager().install())

    def getImages(self):
        url_titlesearch = base_url + '/board_list?keywords=%EC%83%81%EC%84%B8&board=1076&searchKeywordType=THREAD_TITLE'
        self.driver.get(url_titlesearch)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        post_url = base_url + soup.select('body div.list-box a')[0].get('href')

        self.driver.get(post_url)

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        posts = soup.select('body div.board-view div.section-bot div.view-box div.txt.note-editor p')

        if os.path.isdir('./Posts/Images') == False:
            os.mkdir('./Posts/Images')
        [os.remove(f) for f in glob.glob("./Posts/Images/*.png")]
        n=1
        for post in posts:
            img = post.find('img')
            if(img != None) and img.get('width') == '780' and img.get('height') == '438':    
                imgUrl = img.get('src')
                name, ext = os.path.splitext(imgUrl)
                with urllib.request.urlopen(imgUrl) as f:
                    if n<10:
                        str_n = '0' + str(n)
                    else:
                        str_n = str(n)
                    with open('./Posts/Images/' + str_n + '.png', 'wb') as h:
                        img = f.read()
                        h.write(img)
                n += 1
        return post_url

    def getMainTopic(self):
        self.driver.get(base_url)

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        soup_extract = soup.body.extract()
        posts = soup_extract.select('body div.main.main-type2 div.section-bot div.sticky-box ul.swiper-slide.type-list.swiper-slide-active li')

        list_post = []
        for post in posts:
            if post.find('h3') != None:
                # category = post.find('span',class_= 'key-color').text.strip()
                # icon = post.find('span',class_='icon-new')
                title = post.find('h3').text.strip()
                link = post.find('a').get('href')
                date = datetime.strptime(post.find('span', {'class':'date'}).text, '%Y.%m.%d').strftime('%m/%d')
                list_post.append({"title":title, "link":link, "date":date})
        return list_post
    
    def getNotice(self):
        print("test")