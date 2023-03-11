import asyncio
import os
import glob
import aiohttp

from selenium import webdriver
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
        self.driver = webdriver.Edge('edgedriver_win64/msedgedriver.exe', options=options)

    def __del__(self):
        self.driver.quit()

    async def download_image(self, session, url, filename):
        async with session.get(url) as response:
            with open(filename, 'wb') as f:
                async for data in response.content.iter_chunked(1024):
                    f.write(data)
    def getUpdateUrl(self):
        url_search = BASE_URL + '/board_list?keywords=%EC%83%81%EC%84%B8&board=1076&searchKeywordType=THREAD_TITLE'
        self.driver.get(url_search)
        soup_search = BeautifulSoup(self.driver.page_source, 'lxml')
        post_url = BASE_URL + soup_search.select_one('body div.list-box a')['href']
        return post_url

    async def getImages(self,post_url):
        self.driver.get(post_url)
        img_tags = BeautifulSoup(self.driver.page_source, 'lxml', parse_only=SoupStrainer('img', {'width':'780', 'height':'438'})).find_all('img')

        if not os.path.isdir('./Posts/Images'):
            os.mkdir('./Posts/Images')
        
        for file in glob.glob("./Posts/Images/*.png"):
            os.remove(file)

        async with aiohttp.ClientSession() as session:
            tasks = [self.download_image(session, img.get('src'), f"./Posts/Images/{i:02}.png") for i, img in enumerate(img_tags, 1)]
            await asyncio.gather(*tasks)
            
        #  with ThreadPoolExecutor() as executor:
               # tasks = []
            # async with aiohttp.ClientSession() as session:
            #     for i, img in enumerate(img_tags, 1):
            #         img_url = img.get('src')
            #         name, ext = os.path.splitext(img_url)
            #         filename = f"./Posts/Images/{i:02}.png"
            #         tasks.append(asyncio.ensure_future(self.download_image(session, img_url, filename)))
            #     await asyncio.gather(*tasks)
            # return post_url


    def getNotice(self):
        self.driver.get(BASE_URL)
        soup = BeautifulSoup(self.driver.page_source, 'lxml', parse_only=SoupStrainer('li'))

        posts = []
        for soup_child in soup:
            if soup_child.find('h3') is not None:
                title = soup_child.find('h3').text.strip()
                link = BASE_URL + soup_child.find('a').get('href')
                date_str = soup_child.find('span', {'class':'date'})
                try:
                    date = datetime.strptime(date_str.text, '%Y.%m.%d').strftime('%m/%d')
                except ValueError:
                    date = datetime.now().strftime('%m/%d')
                posts.append({"title":title, "link":link, "date":date})

        post_mainTopic = posts[:20]
        post_notice = posts[20:]
        return post_mainTopic, post_notice