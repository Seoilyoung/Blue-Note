from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.request
import os, glob

driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))


url_titlesearch = 'https://forum.nexon.com/bluearchive/board_list?keywords=상세&board=1076&searchKeywordType=THREAD_TITLE'
driver.get(url_titlesearch)
soup = BeautifulSoup(driver.page_source, 'lxml')
post_searched = soup.select('body div.list-box a')[0]
print(post_searched.get('href'))
