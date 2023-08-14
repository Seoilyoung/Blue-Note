import asyncio
import os
import glob
import aiohttp
import re
from selenium import webdriver
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime

BASE_URL = 'https://forum.nexon.com/bluearchive/'

class Posts():
    def __init__(self):
        super().__init__()
        # 옵션 적용
        edge_options = webdriver.EdgeOptions()
        edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        edge_options.add_argument("headless")
        self.driver = webdriver.Edge(options=edge_options)

    async def getUpdateUrl(self):
        url_search = BASE_URL + 'board_list?keywords=상세&board=1076&searchKeywordType=THREAD_TITLE'
        self.driver.get(url_search)
        soup_search = BeautifulSoup(self.driver.page_source, 'lxml')
        post_url = soup_search.select_one('body div.list-box a')
        post_title = post_url.text

        if not os.path.exists('Posts'):
            os.makedirs('Posts')
        if os.path.exists("Posts/.title"):
            with open("Posts/.title", "r", encoding="utf-8") as f:
                current_title = f.read()
            if current_title != post_title:
                with open("Posts/.title", "w", encoding="utf-8") as f:
                    f.write(post_title)
                chk_file =  False
            else:
                chk_file = True
        else:
            with open("Posts/.title", "w", encoding="utf-8") as f:
                    f.write(post_title)
            chk_file = False
        result_url = BASE_URL + post_url['href']

        # 슬라이드쇼 이미지 저장
        if chk_file is False:
            await self.getImages(result_url)
        return result_url

    async def download_image(self, session, url, filename):
        async with session.get(url) as response:
            with open(filename, 'wb') as f:
                async for data in response.content.iter_chunked(1024):
                    f.write(data)

    async def getImages(self, post_url):
        self.driver.get(post_url)
        # img_tags = BeautifulSoup(self.driver.page_source, 'lxml', parse_only=SoupStrainer('img', {'width':'780'})).find_all('img')
        # 사이트 이미지 속성 변경 대응
        img_tags = BeautifulSoup(self.driver.page_source, 'lxml').find_all('img')
        filtered_tags = []
        for img_tag in img_tags:
            if img_tag.has_attr('style'):
                # style 속성에서 width와 height 값을 추출합니다.
                match = re.search(r'width\s*:\s*(\d+)\s*px\s*;\s*height\s*:\s*(\d+)\s*px', img_tag['style'])
                if match:
                    width = int(match.group(1))
                    height = int(match.group(2))
                    # width가 780 이고, height가 400 이상인 경우에 해당하는 이미지를 필터링합니다.
                    if width == 780 and height > 400 and height <500:
                        filtered_tags.append(img_tag)
            elif img_tag.has_attr('width') and img_tag['width'] == '780' and (430 < int(img_tag['height']) and int(img_tag['height']) < 500):
                filtered_tags.append(img_tag)

        if not os.path.exists('Posts'):
            os.makedirs('Posts')
        if not os.path.exists('Posts/Images'):
            os.makedirs('Posts/Images')
        
        for file in glob.glob("./Posts/Images/*.png"):
            os.remove(file)

        async with aiohttp.ClientSession() as session:
            tasks = [self.download_image(session, img.get('src'), f"./Posts/Images/{i:02}.png") for i, img in enumerate(filtered_tags, 1)]
            await asyncio.gather(*tasks)

    async def getNotice(self):
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
                if soup_child.find('span', {'class':'icon-new'}) is not None:
                    new = 1
                else:
                    new = 0
                posts.append({"new":new, "title":title, "link":link, "date":date})

        post_mainTopic = posts[:20]
        post_notice = posts[20:]
        return post_mainTopic, post_notice