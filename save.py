#coding=utf-8
import json
import os

import newsClass
import getNewsContent
from datetime import datetime


NewList = []


def saveData(newsList,totalNum,isCraeteNewFile,fileName,filePath):
    NewList.clear()
    # 获取当前时间
    current_time = datetime.now()
    # 格式化为指定格式的字符串
    formatted_time = current_time.strftime('%Y年%m月%d日 %H:%M')
    # 先获取新闻的具体内容
    i=1
    for news in newsList:
        new = newsClass.News()
        title = news.title
        href = news.href
        new.set_href(href)
        new.set_title(title)
        newsContent = getNewsContent.getContent(href)
        new.set_content(newsContent)
        new.set_time(formatted_time)
        NewList.append(new)
        i=i+1
    # 将集合中的信息写入文件当中
    saveFile(NewList,totalNum,isCraeteNewFile,fileName,filePath)


# 创建文件夹
def create_directory(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

# 保存新闻对象数组到文件
def saveFile(news_collection, totalNum, isCreateNewFile, fileName, filePath):
    # 构建完整文件路径
    full_file_path = os.path.join(filePath, fileName)

    # 如果需要创建新文件夹
    if isCreateNewFile == 1:
        create_directory(full_file_path)

    # 增加序号 index
    for idx, item in enumerate(news_collection, start=totalNum):
        item.index = idx

    # 读取现有JSON文件中的新闻对象数组
    existing_news = []
    if os.path.exists(os.path.join(full_file_path, 'index.json')):
        with open(os.path.join(full_file_path, 'index.json'), 'r', encoding='utf-8') as file:
            existing_news = json.load(file)
    # 合并新闻对象数组
    for item in news_collection:
        existing_news.append({
            "index": item.index,
            "title": item.title,
            "time": item.time,
            "content": item.content
        })

    # 将合并后的新闻对象数组转换为 JSON 格式字符串
    formatted_news_str = json.dumps(existing_news, ensure_ascii=False, indent=4)

    # 将新的 index.json 内容覆盖写入文件
    with open(os.path.join(full_file_path, 'index.json'), 'w', encoding='utf-8') as file:
        file.write(formatted_news_str)




