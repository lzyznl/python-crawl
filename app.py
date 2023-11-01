#coding=utf-8
import sys
import os
from datetime import datetime
import threading
import time
import xml.etree.ElementTree as ET
import pytz
import translate
import requests
import ai
import const
import newsClass
from getNewsContent import getAndPrintContent
from save import saveData

flag=0 # 判断是否第一次打印
lastNumber = -1
genalContent = ''
newsList = []
finalNewsList = []
lastNewsList = []
totalNum = 1
isCreateNewFile = 1 # 是否需要创建新文件，默认是需要
last_time = datetime.now()
newFileName = last_time.strftime("%Y-%m-%d-%H")
gmt8 = pytz.timezone('Asia/Shanghai') # 加载时区信息，提前加载，加快速度

# 进行新闻时间时区转换
def time_converter(input_time):
    input_format = "%a, %d %b %Y %H:%M:%S %Z"
    input_datetime = datetime.strptime(input_time, input_format)

    input_datetime = input_datetime.replace(tzinfo=pytz.utc).astimezone(gmt8)

    output_format = "%Y年%m月%d日 %H:%M"
    output_time = input_datetime.strftime(output_format)

    return output_time

# 创建data目录
def createDataFolder():
    # 获取当前工作目录
    current_directory = os.getcwd()

    # 创建名为 "data" 的文件夹
    data_folder = "data"
    data_path = os.path.join(current_directory, data_folder)

    # 创建文件夹
    os.makedirs(data_path, exist_ok=True)

    # 获取 "data" 文件夹的绝对路径
    absolute_path_to_data = data_path

    return absolute_path_to_data

folderPath = createDataFolder()

# 对初始的所有新闻标题进行抓取
def fetch_url_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("An error occurred during the request:", e)
        return None

# 对抓取到的新闻内容进行初步解析
def extract_item_information(xml_content):
    if xml_content is None:
        return None, None

    newsList.clear()
    finalNewsList.clear()

    root = ET.fromstring(xml_content)

    for item in root.findall(".//item"):  # 取前10个item
        title = item.find("title").text if item.find("title") is not None else ""
        link = item.find("link").text if item.find("link") is not None else ""
        pubTime = item.find("pubDate").text if item.find("pubDate") is not None else ""
        time = time_converter(str(pubTime))
        new = newsClass.News()
        new.set_title(title)
        new.set_href(link)
        new.set_time(time)
        newsList.append(new)
        finalNewsList.append(new)

    return None


# 获取初始新闻入口函数
def periodic_function():
    global flag,lastNewsList,totalNum,isCreateNewFile,newFileName,last_time
    controlNum = 0
    while True:
        # 获取当前时间
        current_time = datetime.now()
        if controlNum==1 and current_time.hour!=last_time.hour: # 此次时间不等于上次时间
            isCreateNewFile = 1 # 将重建文件指示置为1
            totalNum = 1
            # 格式化为指定的字符串形式
            newFileName = current_time.strftime("%Y-%m-%d-%H")
            last_time=current_time
        content = fetch_url_content(const.url)
        extract_item_information(content)
        if(controlNum==0):
            for i in range(0, 10):
                print(str(i + 1) + ':' + newsList[i].title)
            print(const.options1)
            controlNum=1
        flag=1
        # 将数组转化为Set
        lastSet = set(lastNewsList)
        nowSet = set(finalNewsList)
        # 创建线程二：用于处理首次爬取到的新闻信息，然后写入文件
        if len(nowSet.difference(lastSet)) != 0 or isCreateNewFile == 1:
            periodic_thread2 = threading.Thread(target=saveData, args=(nowSet.difference(lastSet),totalNum,isCreateNewFile,newFileName,folderPath))
            periodic_thread2.start()
        # 等待十分钟
        time.sleep(3 * 60)
        isCreateNewFile = 0 # 每一次置1后再次置为0
        totalNum = totalNum+len(nowSet.difference(lastSet))
        lastNewsList.clear()
        for news in finalNewsList:
            lastnew = newsClass.News()
            lastnew.set_title(news.title)
            lastnew.set_content(news.content)
            lastnew.set_href(news.href)
            lastnew.set_time(news.time)
            lastNewsList.append(lastnew)


# 创建线程一，用于每3分钟重新爬取一个新闻
periodic_thread1 = threading.Thread(target=periodic_function)
periodic_thread1.daemon = True  # 将线程设置为守护线程，使得主程序退出时线程也会退出
periodic_thread1.start()

# # 创建线程二：用于处理爬取到的信息，然后写入文件
# periodic_thread2 = threading.Thread(target=saveData)
# periodic_thread2.daemon = True # 设置守护线程
# periodic_thread2.start()


while True:
    if flag == 1:
        user_input = input()
        # user_input = '0'
        if user_input.isdigit() and 1 <= int(user_input) <= 10:
            os.system("clear")
            flag1=0
            print('新闻标题:'+finalNewsList[int(user_input)-1].title)
            print('新闻链接:'+finalNewsList[int(user_input)-1].href)
            print('具体新闻内容如下:(或许需要2-3s)')
            genalContent=''
            content = getAndPrintContent(finalNewsList[int(user_input)-1].href)
            print(const.options2)
            lastNumber=int(user_input)
            genalContent += content
        elif user_input.lower() == 't':
            os.system("clear")
            if genalContent == '':
                print('你还未选择新闻')
            else:
                target_language = "zh"  # 中国简体中文
                translated_text = translate.translate_japanese_to_chinese(str(genalContent))
                print('翻译结果为:')
                print(translated_text)
                print(const.options3)
        elif user_input.lower() == 'r':
            os.system("clear")
            for i in range(0, 10):
                print(str(i + 1) + ':' + finalNewsList[i].title)
            print(const.options1)
        elif user_input.lower() == 's':
            os.system("clear")
            content = str(const.word) + str(genalContent)
            AIContent = ai.getAIAnswer(content)
            print("总结后的新闻内容是:")
            print(AIContent)
            print(const.options4)
        elif user_input.lower() == 'q':
            exit()
        else:
            print("无效输入，请重新输入")





