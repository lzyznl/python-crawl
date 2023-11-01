#coding=utf-8

import requests
from bs4 import BeautifulSoup



# 用户查看新闻时爬取新闻内容
def scrape_yahoo_news_content(url):
    try:
        # 发送HTTP请求并获取页面内容
        response = requests.get(url)
        if response.status_code != 200:
            print("Failed to retrieve the webpage. Status code:", response.status_code)
            return None

        # 使用BeautifulSoup解析页面内容
        soup = BeautifulSoup(response.content, 'html.parser')

        # 找到指定class的元素
        target_elements = soup.find_all(class_='sc-iMCRTP ePfheF yjSlinkDirectlink highLightSearchTarget')

        if not target_elements:
            print("No elements found with the specified class.")
            return None

        # 提取元素的文本内容
        content = [element.get_text() for element in target_elements]
        return content

    except requests.exceptions.RequestException as e:
        print("An error occurred during the request:", e)
        return None

# 打印新闻内容
def getAndPrintContent(url):
    content = scrape_yahoo_news_content(url)
    rcontent = ''
    if content:
        for idx, item in enumerate(content, start=1):
            print(item)
            rcontent+=item
        return rcontent

# 获取新闻内容
def getContent(url):
    content = scrape_yahoo_news_content(url)
    rcontent = ''
    if content:
        for idx, item in enumerate(content, start=1):
            rcontent+=item
        return rcontent