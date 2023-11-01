#coding=utf-8

import random
from hashlib import md5
import requests
import const


# 辅助函数：生成MD5签名
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

# 主要翻译函数
def translate_japanese_to_chinese(text):
    salt = random.randint(32768, 65536)
    sign = make_md5(const.bd_appid + text + str(salt) + const.bd_appkey)

    # 构造请求参数
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        'appid': const.bd_appid,
        'q': text,
        'from': const.from_lang,
        'to': const.to_lang,
        'salt': salt,
        'sign': sign
    }

    # 发送请求并获取响应
    response = requests.post(const.urls, params=payload, headers=headers)
    result = response.json()

    # 解析翻译结果
    translations = []
    if 'trans_result' in result:
        for item in result['trans_result']:
            translations.append(item['dst'])

    return '\n'.join(translations)