from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import os,shutil, glob

url = 'https://forum.nexon.com/bluearchive/board_view?board=1076&thread=2035425&stickyBoard=1'

options = webdriver.EdgeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Edge('msedgedriver.exe',options=options)
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'lxml')
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
