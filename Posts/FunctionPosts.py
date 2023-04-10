import asyncio
import os
import glob
import aiohttp
import re
import requests
import zipfile
import io
from selenium import webdriver
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime

BASE_URL = 'https://forum.nexon.com/bluearchive/'

class Posts():
    def __init__(self):
        super().__init__()

        # 웹 드라이버 버전 확인을 위한 URL
        response = requests.get("https://msedgedriver.azureedge.net/LATEST_STABLE")
        version = response.text.strip()
        driver_path = './webdrivers/msedgedriver.exe'
        with open("webdrivers/.version", "r") as f:
            current_version = f.read()
        # 최신 버전 다운로드 링크 생성
        if current_version != version:
            url = f"https://msedgedriver.azureedge.net/{version}/edgedriver_win64.zip"
            response = requests.get(url)
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                zip_ref.extractall("webdrivers")
            os.chmod(driver_path, 0o755)
            with open("webdrivers/.version", "w") as f:
                f.write(version)

        # 옵션 적용
        edge_options = webdriver.EdgeOptions()
        edge_options.add_argument("disable-logging")
        edge_options.add_argument("headless")
        self.driver = webdriver.Edge(executable_path=driver_path, options=edge_options)

    def getUpdateUrl(self):
        url_search = BASE_URL + 'board_list?keywords=상세&board=1076&searchKeywordType=THREAD_TITLE'
        self.driver.get(url_search)
        soup_search = BeautifulSoup(self.driver.page_source, 'lxml')
        post_url = BASE_URL + soup_search.select_one('body div.list-box a')['href']
        return post_url

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
        if not os.path.isdir('./Posts/Images'):
            os.mkdir('./Posts/Images')
        
        for file in glob.glob("./Posts/Images/*.png"):
            os.remove(file)

        async with aiohttp.ClientSession() as session:
            tasks = [self.download_image(session, img.get('src'), f"./Posts/Images/{i:02}.png") for i, img in enumerate(filtered_tags, 1)]
            await asyncio.gather(*tasks)

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
                if soup_child.find('span', {'class':'icon-new'}) is not None:
                    new = 1
                else:
                    new = 0
                posts.append({"new":new, "title":title, "link":link, "date":date})

        post_mainTopic = posts[:20]
        post_notice = posts[20:]
        return post_mainTopic, post_notice