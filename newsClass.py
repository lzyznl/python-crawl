#coding=utf-8

class News:
    def __init__(self):
        self.title = None  # 新闻标题
        self.href = None  # 新闻链接
        self.content = None  # 新闻内容
        self.time = None  # 新闻时间

    def __eq__(self, other):
        return self.title == other.title and self.content == other.content and self.href == other.href

    def __hash__(self):
        return hash((self.title, self.content))

    def set_title(self, title):
        self.title = title

    def set_href(self, href):
        self.href = href

    def set_content(self, content):
        self.content = content

    def set_time(self,time):
        self.time = time