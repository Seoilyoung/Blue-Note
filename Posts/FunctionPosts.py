import asyncio
import os
import glob
import aiohttp

from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

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

    async def download_image(self, session, url, filename):
        async with session.get(url) as response:
            with open(filename, 'wb') as f:
                async for data in response.content.iter_chunked(1024):
                    f.write(data)

    async def getImages(self):
        url_search = BASE_URL + '/board_list?keywords=%EC%83%81%EC%84%B8&board=1076&searchKeywordType=THREAD_TITLE'
        self.driver.get(url_search)
        soup_search = BeautifulSoup(self.driver.page_source, 'lxml')
        post_url = BASE_URL + soup_search.select_one('body div.list-box a')['href']

        self.driver.get(post_url)

        img_tags = BeautifulSoup(self.driver.page_source, 'lxml', parse_only=SoupStrainer('img', {'width':'780', 'height':'438'})).find_all('img')

        if not os.path.isdir('./Posts/Images'):
            os.mkdir('./Posts/Images')
        
        for file in glob.glob("./Posts/Images/*.png"):
            os.remove(file)

        with ThreadPoolExecutor() as executor:
            tasks = []
            async with aiohttp.ClientSession() as session:
                for i, img in enumerate(img_tags, 1):
                    img_url = img.get('src')
                    name, ext = os.path.splitext(img_url)
                    filename = f"./Posts/Images/{i:02}.png"
                    tasks.append(asyncio.ensure_future(self.download_image(session, img_url, filename)))
                await asyncio.gather(*tasks)

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
        
    # async def getNotice(self):
    #     print("test")