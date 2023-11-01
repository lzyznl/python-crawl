#coding=utf-8

# 一些所需参数
url = "https://news.yahoo.co.jp/rss/categories/life.xml"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}
# 百度翻译API参数
bd_appid = '20231007001839386'  # 替换为你的百度翻译API应用ID
bd_appkey = 'LIKxDadYENAgI5AoGUaM'  # 替换为你的百度翻译API应用密钥
from_lang = 'jp'
to_lang = 'zh'
urls = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
word = '你好，我想尽快的得到一段日文新闻所表达的主旨内容，所以我将会给你一段日文新闻，请你先将这段日文新闻翻译为中文后，进行内容概括，概括为30字以内，一定要是30字以内，然后返回概括后的中文内容，具体提供给你的新闻内容如下：'

# 以下密钥信息从控制台获取
appid = "4b336d8b"  # 填写控制台中获取的 APPID 信息
api_secret = "MDkwODQyNmJkOWQxYmI4NWI2ZjlhM2Nj"  # 填写控制台中获取的 APISecret 信息
api_key = "4fd0f6bb796decab010247e3200e6717"  # 填写控制台中获取的 APIKey 信息

# 用于配置大模型版本，默认“general/generalv2”
#domain = "general"  # v1.5版本
domain = "generalv2"    # v2.0版本
# 云端环境的服务地址
# Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址

options1 = (
    "----------选择操作:--------------------\n"
    "--        1-10: 查看新闻             --\n"
    "--        q: 退出                    --\n"
    "----------请输入您的选择:--------------\n"
)

options2 =(
    "---------------------------------------\n"
    "--          t: 翻译为中文            --\n"
    "--          r: 返回新闻列表          --\n"
    "--          q: 退出                  --\n"
    "---------------------------------------\n"
)

options3 =(
    "----------------------------------------\n"
    "--          s: 概括新闻内容           --\n"
    "--          r: 返回新闻列表           --\n"
    "--          q: 退出                   --\n"
    "----------------------------------------\n"
)

options4 =(
    "----------------------------------------\n"
    "--          r: 返回新闻列表           --\n"
    "--          q: 退出                   --\n"
    "----------------------------------------\n"
)
